''' Created on May 22, 2015 @author: Barbara Munoz '''

import sqlite3
import cv2
import numpy as np
import sys
import db


def analysisParkingSpot ():
 
    ''' Initialise the camera '''
    initCam = cv2.VideoCapture(1)
    
    ''' Takes a screenshot and convert it from RGB A HSV '''
    _, photo = initCam.read()
    cv2.imwrite('photo.jpg',photo)
    hsv = cv2.cvtColor(photo,cv2.COLOR_BGR2HSV)
    #cv2.imshow('hsv',hsv)

    ''' Color range of green to be detected in HSV
    Color values in RGB type, specified in 'dtype' '''
    lower_Color = np.array([0,250,0], dtype=np.uint8)
    upper_Color = np.array([190,255,100], dtype=np.uint8)
    
    ''' Mask creation for detecting the color range '''
    mask = cv2.inRange(hsv, lower_Color,upper_Color)
    #cv2.imshow('mask',mask)

    ''' Filtering the noise with an CLOSE/OPEN '''
    kernel = np.ones((6,6), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernel)
    #cv2.imshow('openclose',mask)
    
    ''' Blur the mask to soften the edges '''
    blur = cv2.GaussianBlur(mask,(5,5),0)
    #cv2.imshow('blur',blur)
    
    ''' Canny '''
    edges = cv2.Canny(mask,1,2)
    #cv2.imshow('edges',edges)
    
    ''' Contours detection '''
    ''' CONTOURS is a list which contains the coordinates of the points of each contour
        HIERARCHY contains the contour hierarchy '''
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ''' Saves the contours detected '''
    areas = [cv2.contourArea(c) for c in contours] 
   
    ''' Check if the areas are bigger than 600px 
        Elimination of noise and false positives '''
   
    i = 0; j=0
    areaSpot = []
    
    for extension in areas:
        if extension > 600:
            actual = contours[i]
            ''' Approx the number of corners '''
            approx = cv2.approxPolyDP(actual, 0.05*cv2.arcLength(actual,True),True) 
            ''' If has 4 corners is a rectangle '''
        if len(approx)== 4:
            cv2.drawContours(photo,[actual],0,(0,250,200),2)
            areaSpot.append(extension)  
            j += 1   
                  
        i = i+1
  
    return areaSpot


#Compares the empty parking lot with the actual parking situation
#in this way we know if a space is occupied or free
#It basically does a difference between two different images taken 
# at two different times at the same parking lot

def parkingSituation (areaVector = []):
    areaVectorOriginal = [27027.0, 26730.0, 26730.5, 27570.5]
    posti = ['OCCUPIED','OCCUPIED','OCCUPIED','OCCUPIED']
    if (len(areaVector) > 0) :  
        k=0 
        for a in areaVectorOriginal:
            for b in areaVector:
                if a == b:
                    posti[k]= "FREE"
            k +=1   
    else:
        print "PARKING FULL"
        p=0
        for posto in posti:
            posti[p] = "OCCUPIED"  
            p += 1    
    return  posti  

def dbUpdate(cur, conn, parkingStatus=[]):
     
    #Sets 0 is the space is empty, sets 1 if is occupied          
    n=0 
    for posto in parkingStatus:
        n+=1 
        if (posto=='FREE'):
            #queryCurs.execute("UPDATE easypark SET AVAILABILITY=? WHERE ID=?", (0,n)) 
            db.update_status(cur, conn, 1, n, 0)
        elif (posto=='OCCUPIED'): 
            db.update_status(cur, conn, 1, n, 1)
    #       queryCurs.execute("UPDATE easypark SET AVAILABILITY=? WHERE ID=?", (1,n))  
   
    
    #####debug####
    print "\n"
    print "CURRENT PARKING SITUATION: \n"  
    data=db.all_park_status(cur, conn, 1)
    #for i in queryCurs:
    for i in db:
        print "\n"
        for j in i:
            print j


