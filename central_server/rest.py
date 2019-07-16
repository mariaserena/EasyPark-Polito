'''
Created on May 18, 2015

@author: mariaserena
'''
import urllib2, json

def send(method = 'GET', url=None, data = None, headers = {}):
    #the response dictionary, initially empty
    response_dict = dict()
    
    #check that the url is not empty
    if(url!=None):
        #build the request
        req = urllib2.Request(url, data, headers)
        req.get_method = lambda: method
       
        
        #try to call the url
        result = None
        try:
            #get the result
            result = urllib2.urlopen(req)
        except urllib2.URLError, e:
            #print the error
            print "response was: "
            print e.reason
        
        #check result
        if(result != None):
            #decode the result
            result_as_string = result.read().decode('utf8')

            
            if(result_as_string != ''):
                #convert the response into a dictionary
                response_dict = json.loads(result_as_string)
                print response_dict
    
    return response_dict