'''
Created on Jun 23, 2015

@author: mariaserena
'''
from flask import Flask
from flask import render_template
import rest, time
from subprocess import Popen, PIPE
from thread import start_new_thread

########global variables#####
parking_id=1
basic_url='http://192.168.1.132:5000'
users_url='/easypark/api/v1.0/users?plate='
directions_url='/easypark/api/v1.0/directions?parking='

user=None
directions=None
plate_detec_program_name='alpr '
plate_detec_parameters='-c eu -n 1'
cam_program_name='fswebcam '
cam_parameters='--no banner '
file_path='/home/pi/Desktop/img2.jpg'
#######################app###################################
app=Flask(__name__)

@app.route('/welcome')
def index():
    return render_template("index.html", user=user, directions=directions)

#####################thread function#############
def thread_func():
    prev_plate=None
    new_plate=None
    global user
    global directions
    
    while(True):
        #it makes a photo and substitute the old one
        Popen(cam_program_name+cam_parameters+file_path, stdin=PIPE, stdout=PIPE, shell=True)
        #calls the detect plate
        new_plate=detect_plate()
        #if openalpr does not find any plates, it changes variables: no car in entrance
        if(new_plate == None):
            user=None
            directions=None
        #if openlapr finds a plate different from the previous one, it changes variables: new car in entrance
        elif(new_plate!=None and new_plate!=prev_plate):
            #it calls the central server
            url_to_use=basic_url+users_url+new_plate
            user=rest.send(method='GET',url=url_to_use, headers={'Accept':'application/json'})
            
            url_to_use=basic_url+directions_url+parking_id
            directions=rest.send(method='GET', url=url_to_use, headers={'Accept':'application/json'})
            #cambia vecchie variab con nuove:
            prev_plate=new_plate
        #if openalpr find the prevoius plate, it does nothing
        
        #sleep 5 sec
        time.sleep(4)
    
############################main##############
def detect_plate():
    
    result=Popen(plate_detec_program_name+plate_detec_parameters+file_path, stdin=PIPE, stdout=PIPE, shell=True)
    (output, error)=result.communicate()#debug
    exit_code=result.wait()
   
    #check the exit code
    if(exit_code!=0) or not ("plate" in output):
        nplate=None
    elif "plate" in output:
        res=output.split()
        nplate=res[4]
    return nplate
       
def main():
    
    app.run(debug=True)
    
    start_new_thread(thread_func)
        
    
if __name__ == '__main__':
    main()
