import paho.mqtt.client as mqtt
import requests
import os
import time 

from dotenv import load_dotenv

##########################
## HELPERS ###############
###########################
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

load_dotenv()
port = os.getenv("PORT")
addr = os.getenv("ADDR")
mqtt_addr = os.getenv("MQTT_ADDR")
mqtt_port= os.getenv("MQTT_PORT")
mqtt_user= os.getenv("MOSQUITTO_USER")
mqtt_pwd= os.getenv("MOSQUITTO_PWD")

subscribed_topics = []

##############################
###### INIT PROGRAM #########
##############################

def populate():
    topics = {}
    populated = False
    url = "http://" + addr + ":" + port + "/sensors"
    try:
        r = requests.get(url)
        # Populate sensors with required information
        for sensor in r.json()["Sensors"]:
            name = sensor[0]
            topics[name]= True
        populated = not populated 
    except Exception as e:
        print(bcolors.FAIL + "Exception raised while requesting for topics" + bcolors.ENDC)
        return {}, False
    return topics, True

def block_populate_topics():
    topics = {}
    populated = False 
    while not populated:
        print(bcolors.HEADER + "Trying to populate topics to subscribe to.." + bcolors.ENDC)
        topics, populated = populate()
        print(bcolors.WARNING + "Waiting 2 seconds to populate topics..." + bcolors.ENDC)
        time.sleep(2)
    print(bcolors.OKBLUE + "Topics have been populated: {}".format(topics) + bcolors.ENDC)
    return topics

def send_data(data):
    port = os.getenv("PORT")
    addr = os.getenv("ADDR")
    url = "http://" + addr + ":" + port + "/records"
    r = requests.post(url, json=data)
    return r.status_code


#################################
##### MQTT METHOD DEFINITION ####
#################################
def on_connect(client, userdata, flags, rc):
    # Called once the client connect
    print("Connected with result code {0}".format(str(rc)))
    print(bcolors.HEADER + "Populating topics to subscribe to..." + bcolors.ENDC)
    subscribed_topics = block_populate_topics()
    client.subscribe('#')
    # Subscription here
    for topic in subscribed_topics:
        client.subscribe(topic)


def on_message(client, userdate, msg):
    topic = msg.topic
    payload = int(msg.payload.decode("utf-8"))
    data = {"sensor_type": topic, "value": payload}
    status_code = send_data(data)
    print("Received value {} from topic {} with status code {}".format(payload, topic, status_code))

client = mqtt.Client("sub-mqtt")  # Client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqtt_user, mqtt_pwd)
client.connect(mqtt_addr, int(mqtt_port))
client.loop_forever()