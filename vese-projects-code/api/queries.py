# Queries

## Create a new sensors
CREATE_SENSOR="INSERT INTO sensors (name, min, max, min_safe, max_safe) VALUES(?,?,?,?,?)"

## getSensors
GET_SENSORS="SELECT * FROM sensors"

## getSensorByName
GET_SENSOR_BY_NAME="SELECT * FROM sensors WHERE name = ?"

## setSensorValueByName
SET_SENSOR_BY_NAME="UPDATE sensors SET min = ?, max = ? WHERE name = ?"

## Create record
CREATE_RECORD="INSERT INTO records (sensor_type, value) VALUES (?, ?)"

## getRecords
GET_RECORDS="SELECT * FROM records ORDER BY date DESC LIMIT 10"

## getMaxRecordByName (sensor)
GET_MAX_RECORDS_BY_NAME="SELECT * FROM records WHERE sensor_type = ? ORDER BY VALUE DESC LIMIT 10"


## getMinRecordByName (sensor)
GET_MIN_RECORDS_BY_NAME="SELECT * FROM records WHERE sensor_type = ? ORDER BY VALUE ASC LIMIT 10"