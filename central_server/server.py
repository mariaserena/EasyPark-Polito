'''
Created on May 18, 2015

@author: mariaserena
'''
import sqlite3
from flask import Flask, request, json, jsonify
import db
import time
from thread import start_new_thread
import procedureDefinition

app = None
conn = sqlite3.connect('easypark.db', check_same_thread=False)
cur = conn.cursor()
app = Flask(__name__)   

numb_parkings=3;


#db.prepare_all(cur, conn) #it makes the table in the db

#-----app-----
@app.route('/')
def index():
    return db.all_users(cur, conn)
#-------rest server----- 
@app.route('/easypark/api/v1.0/users', methods=['GET'])
def get_user_from_nplate():
    plate = request.args.get('plate')
    user=db.user_from_nplate(cur, conn, plate)
    res={"user": user}
    return jsonify(res)

@app.route('/easypark/api/v1.0/user', methods=['GET'])
def check_user():
    username = request.args.get('username')
    password = request.args.get('password')
    resp=db.check_user(cur, conn, username, password)
    res={"response": resp}
    return jsonify(res)

@app.route('/easypark/api/v1.0/users/new', methods=['POST'])
def new_user():
    data=request.get_json(force=True)
    resp=db.add_new_user(cur, conn, data['name'], data['surname'], data['username'], data['password'], data['nplate'])
    return jsonify({"response": resp})
    
    
   
@app.route('/easypark/api/v1.0/directions' , methods=['GET'])
def get_directions():
    id = request.args.get('parking')
    dir=db.directions(cur, conn, id) 
    return jsonify({"directions": dir})

        
@app.route('/easypark/api/v1.0/parkings', methods=['GET'])
def get_parkings():
    parking_spaces={}
    #for all the parkings return the availability
    for i in range(1, numb_parkings+1):
        parking_spaces.update({str(i) : db.count_free_spaces(cur, conn, str(i))})
    
    
    return jsonify(parking_spaces) 

################################thread function##################
def thread_func():
    #the function that updates the db is called here
    while(True):
        ''' Calls analysisParkingSpot procedure and saves the output on areaVector '''
    areaVector = procedureDefinition.analysisParkingSpot
    
        ''' Execute parkingSituation using areaVector as an input
        ParkingStatus contains a vector with the status of each parking space'''
    parkingStatus = procedureDefinition.parkingSituation(areaVector)
        ''' Updates the data base with the current parking status '''
    procedureDefinition.dbUpdate(parkingStatus)


        time.sleep(60)

if (__name__=='__main__'):
    app.run(host='0.0.0.0')
    #app.run(debug=True)
    
    start_new_thread(thread_func)
