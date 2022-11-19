import queries
from flask import jsonify, request

def init_views(app, db):

    ################
    #    SENSORS   #
    ################

    @app.route('/sensors', methods=["POST"])
    def createSensor():
        '''
            Creates a new sensor and inserts it into database.
            @retuns ... 
        '''
        body = request.get_json()
        data = db.createSensor(body)
        return jsonify({"Creating a new sensor...": data})


    @app.route('/sensors', methods=["GET"])
    def getSensors():
        '''
            Get all sensors data from database.
            @return Array with all sensors actually stored
        '''
        return jsonify({"Sensors": db.getSensors() })


    @app.route('/sensors/<name>', methods=["GET"])
    def getSensorByName(name):
        '''
            Get data from a specific sensor from database.
            @params 
                - @name : Name of the sensor to retrieve.
            @return 
        '''
        data = db.getSensorByName(name)
        if not data:
            return jsonify({"Message": "Not found", "CodeStatus": 404}) 
        return jsonify({"Sensors": data})

    @app.route('/sensors/<name>', methods=["PUT"])
    def setSensorValuesByName(name):
        '''
            Change sensors data. 
            It only allows to change MIN, MAX, MIN_SAFE, MAX_SAFE columns
            @params
                - @name: Id name of the sensor to retrieve. 
        '''
        body = request.get_json()
        data = db.setSensorByName(name, body)
        return jsonify({"Sensors": data})
        


    ################
    #    RECORDS   #
    ################

    @app.route('/records', methods=["POST"])
    def addRecord():
        '''
            Creates a new record and inserts it into database.
            @retuns ... 
        '''
        print("Creating record...")
        body = request.get_json()
        data = db.createRecord(body)
        return jsonify({"Creating a new record...": data}) 

    @app.route('/records', methods=["GET"])
    def getRecords():
        '''
            Gets all records from database. 
            @returns: All records data in JSON form. (Should be limited)
        '''
        data = db.getRecords()
        return jsonify({"Records": data})
                

    @app.route('/records/max/<name>', methods=["GET"])
    def getMaxRecordsByName(name):
        '''
            @returns: Maximum (X) values from records of @name sensor. 
        ''' 
        data = db.getMaxRecordsByName(name)
        return jsonify({"Max values from sensor": data})
        

    @app.route('/records/min/<name>', methods=["GET"])
    def getMinRecordsByName(name):
        '''
            @returns: Minimum (X) values from records of @name sensor. 
        ''' 
        data = db.getMinRecordsByName(name)
        return jsonify({"Min values from sensor": data})




