from dataclasses import dataclass
from queries import CREATE_SENSOR, CREATE_RECORD, GET_MIN_RECORDS_BY_NAME, SET_SENSOR_BY_NAME, GET_SENSORS, GET_MAX_RECORDS_BY_NAME, GET_RECORDS, GET_SENSOR_BY_NAME
import mariadb
import os
import sys

class Database:

    conn = None

    def __init__(self):
       self.connect()
    
    def connect(self):
        try:
            conn = mariadb.connect(
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PWD"),
                host = os.getenv("DB_HOST"),
                port = int(os.getenv("DB_PORT")),
                database= os.getenv("DB_NAME"),
            )
        except mariadb.Error as e:
            print("Error connecting to Mariadb database\n {}".format(e))
            sys.exit(1)

        self.conn = conn # Setting connection
    
    def close(self):
        self.conn.close() # Closes database connection.

    @classmethod
    def execute_query(cls, connection, query, params):
        data = []
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query,params)
            else:
                cursor.execute(query)
            data = "OK" if cursor.description is None else cursor.fetchall()
            connection.commit()
        
        except mariadb.Error as e:
            connection.rollback()
            return "Internal error: {}".format(e)
        if not cursor.closed: 
            cursor.close()
        return data
            
    ###############
    ### SENSORS ###
    ###############
    
    def createSensor(self, sensor):
        name = sensor["name"]
        min = sensor["min"]
        max = sensor["max"]
        min_safe = sensor["min_safe"]
        max_safe = sensor["max_safe"]
        params = (name, min, max, min_safe, max_safe)
        print(params)
        data = Database.execute_query(self.conn, CREATE_SENSOR, params)

        return data 

    def getSensors(self):
        data = Database.execute_query(self.conn, GET_SENSORS, None)
        return data 

    def getSensorByName(self, name):
        data = Database.execute_query(self.conn, GET_SENSOR_BY_NAME,(name,))
        return data
    
    def setSensorByName(self, name, body):
        min = body["min"]
        max = body["max"]
        params = (min, max, name)
        data = Database.execute_query(self.conn, SET_SENSOR_BY_NAME, params)
        return data

    #####################
    ####### RECORDS #####
    #####################

    def createRecord(self, record):
        sensor_type = record["sensor_type"] 
        value = record["value"]
        params = (sensor_type, value)
        data = Database.execute_query(self.conn, CREATE_RECORD, params)
        return data
    
    def getRecords(self):
        data = Database.execute_query(self.conn, GET_RECORDS, None)
        return data

    def getMaxRecordsByName(self, name):
        data = Database.execute_query(self.conn, GET_MAX_RECORDS_BY_NAME, (name,))
        return data
        
    def getMinRecordsByName(self, name):
        data = Database.execute_query(self.conn, GET_MIN_RECORDS_BY_NAME, (name,))
        return data