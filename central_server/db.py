'''
Created on May 18, 2015

@author: mariaserena
'''
import sqlite3
import json

# 0 libero 1 occupato

def prepare_all(cur, conn):
    #create users table
    cur.execute("CREATE TABLE USERS (NAME text NOT NULL, SURNAME text NOT NULL, USERNAME text PRIMARY KEY NOT NULL, PASSWORD text NOT NULL, NPLATE text NOT NULL)")
    
    #Crete parking tables
    cur.execute('''CREATE TABLE PARKING1 (ID int PRIMARY KEY NOT NULL,AVAILABILITY int NOT NULL,DIRECTIONS text NOT NULL)''')
    cur.execute('''CREATE TABLE PARKING2 (ID int PRIMARY KEY NOT NULL,AVAILABILITY int NOT NULL,DIRECTIONS text NOT NULL)''')
    cur.execute('''CREATE TABLE PARKING3 (ID int PRIMARY KEY NOT NULL,AVAILABILITY int NOT NULL,DIRECTIONS text NOT NULL)''')
    
    
    #4 users:
    cur.execute("INSERT INTO USERS VALUES('barbara','munoz','barbara_m', 'hola', 'XB5827')")
    cur.execute("INSERT INTO USERS VALUES('serena', 'ciaburri', 'm_serena', 'cerreto', '2DRT32')")
    cur.execute("INSERT INTO USERS VALUES('lorenzo', 'chianura', 'lorenzo_c', 'metal', '22TY33')")
    cur.execute("INSERT INTO USERS VALUES('cristina', 'donato', 'cristina_d', 'stracciatella', '34GT62')")
    cur.execute("INSERT INTO USERS VALUES('raffaele', 'gemiti', 'raffa_gem', 'juventus', '75TZ54')")
    conn.commit()
    
    #insert 4 free spaces in paring1 
    cur.execute("INSERT INTO PARKING1 VALUES(1,0,'immediately on the right')")
    cur.execute("INSERT INTO PARKING1 VALUES(2,0,'immediately on the left')")
    cur.execute("INSERT INTO PARKING1 VALUES(3,0,'ahead on the left')")
    cur.execute("INSERT INTO PARKING1 VALUES(4,0,'ahead on the right')")
    conn.commit()
    
    #insert 2 free spaces in parking2
    cur.execute("INSERT INTO PARKING2 VALUES(1,0,'immediately on the right')")
    cur.execute("INSERT INTO PARKING2 VALUES(2,0,'immediately on the left')")
    cur.execute("INSERT INTO PARKING2 VALUES(3,1,'ahead on the left')")
    cur.execute("INSERT INTO PARKING2 VALUES(4,1,'ahead on the right')")
    conn.commit()
    
    #insert 2 spaces in parking3
    cur.execute("INSERT INTO PARKING3 VALUES(1,1,'on the left')")
    cur.execute("INSERT INTO PARKING3 VALUES(2,0,'on the right')")
    conn.commit()
    
    conn.close()
    
    
###################################DATABASE FUNCTIONS################################################################    
#insert a new user in the db    
def add_new_user(cur, conn, name, surname, username, password, nplate):
    cur.execute("INSERT INTO USERS VALUES(?,?,?,?,?)", (name, surname, username, password, nplate))
    conn.commit()
    return json.dumps('Inserted')

#show all the users    
def all_users(cur, conn):
    cur.execute("SELECT * FROM USERS")
    rows=cur.fetchall()
    return json.dumps(rows)

#check a user exists
def check_user(cur, conn, username, password):
    cur.execute('SELECT * FROM USERS WHERE USERNAME=? AND PASSWORD=?',[username, password])
    name=cur.fetchone()
    if name is None:
        return json.dumps('NotFound')
    else:
        return json.dumps('Found')

#show all the spaces in a parking lot
def all_spaces(cur, conn, park_id):
    string_query='SELECT * FROM PARKING'+park_id
    print string_query
    cur.execute(string_query)
    rows=cur.fetchall()
    conn.commit()
    return json.dumps(rows)

#find the user corresponding to a number plate
def user_from_nplate(cur, conn, nplate):
    
    cur.execute('SELECT NAME FROM USERS WHERE NPLATE=?', [nplate])
    name=cur.fetchone()
    
    if name is None:
        return json.dumps('None')
    else:
        return json.dumps(name)

#find the closest available spot in a parking (id) and return directions
def directions(cur, conn, park_id):
    string_query='SELECT DIRECTIONS FROM PARKING'+park_id+' WHERE AVAILABILITY=0 LIMIT 1 '
    cur.execute(string_query)
    data=cur.fetchone()
    print 'data'
    print data
    return json.dumps(data)
   

#count the free spaces in a specific parking lot (id)
def count_free_spaces(cur, conn, id):
    parking_name='parking'+id
    query_string='SELECT COUNT(*) FROM '+parking_name.upper()+' WHERE AVAILABILITY=0'
    cur.execute(query_string)
    data=cur.fetchone()
    return data
        

#update status of a parking -given a parking and an id
def update_status(cur, conn, park_id, space_id, space_status):
    parking_name='parking'+park_id
    query_string='UPDATE FROM '+parking_name.upper()+' SET AVAILABILITY='+space_status+' WHERE ID='+space_id
    cur.execute(query_string)
    conn.commit()
    
#return the status of all the spaces in a parking lot -debug
def all_park_status(cur, conn, park_id):
    parking_name='parking'+park_id
    query_string='SELECT * FROM '+parking_name.upper()
    cur.execute(query_string)
    data=cur.fetchall()
    return data

