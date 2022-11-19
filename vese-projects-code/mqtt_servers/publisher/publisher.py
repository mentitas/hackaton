import os
import random 
import time

from paho.mqtt import client as mqtt_client
import requests
from dotenv import load_dotenv

##############################
###      INIT PROGRAM      ###
##############################

load_dotenv()


mqtt_addr = os.getenv("MQTT_ADDR")
mqtt_port= os.getenv("MQTT_PORT")
mqtt_user= os.getenv("MOSQUITTO_USER")
mqtt_pwd= os.getenv("MOSQUITTO_PWD")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def populate():
    topics = {}
    populated = False
    url = "http://" + addr + ":" + port + "/sensors"
    try:
        r = requests.get(url)
        # Populate sensors with required information
        for sensor in r.json()["Sensors"]:
            name = sensor[0]
            min, max = sensor[1], sensor[2]
            topics[name]= { "min": min, "max": max}
        populated = not populated 
    except Exception as e:
        print(bcolors.FAIL + "Exception raised while requesting for topics" + bcolors.ENDC)
        return {}, False
    return topics, True

##############################
### MQTT METHOD DEFINITION ###
##############################

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d", rc)


#######################
#### CLIENT INIT  #####
#######################


client = mqtt_client.Client(client_id="pub.mqtt", transport="tcp")
client.username_pw_set(mqtt_user, mqtt_pwd)
client.on_connect = on_connect
client.connect(mqtt_addr, int(mqtt_port))


########################
##### GET TOPICS #######
########################


port = os.getenv("PORT")
addr = os.getenv("ADDR")



topics = {}
populated = False 
while not populated:
    print(bcolors.HEADER + "Trying to populate topics to create mock data for sensors..." + bcolors.ENDC)
    topics, populated = populate()
    print(bcolors.WARNING + "Waiting 5 seconds to populate topics..." + bcolors.ENDC)
    time.sleep(5)

print(bcolors.OKBLUE + "Topics have been populated: {}".format(topics) + bcolors.ENDC)

####################
#### LOOP ##########
####################
client.loop_start()
i = 0 
while True:
    time.sleep(2) 
    for topic in topics.keys():
        minT, maxT = topics[topic]["min"], topics[topic]["max"]
        data = random.randrange(minT, maxT)
        res = client.publish(topic, data)
        status = res[0]
        if status == 0:
            print("Sent {} to {}".format(data, topic))
        else:
            print(bcolors.FAIL + "Failed to send data to topic {}".format(topic) + bcolors.ENDC)
    i = i + 1
    if i >= 5:
        i = 0
        newTopics, isPopulated = populate()
        if isPopulated:
            topics = newTopics
            print(bcolors.OKGREEN + "Repopulated topics successfully!" + bcolors.ENDC)