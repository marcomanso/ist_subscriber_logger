#!/usr/local/bin/python3

import paho.mqtt.client as mqtt
import argparse
import json
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG)

# PLEASE SET local_COUNTRY to use your own COUNTRY code before running the script.
#
# rationale => if matched to a received message's COUNTRY, the message will be logged as "sent" instead of "received"
local_COUNTRY = 'DEU'

#global variable storing MQTT parameters
mqtt_data = {}

#global variable storing NODE parameters
node_data = {}

#global variable for file used to store log data
log_file_location = None

#global variable to indicate IDs of receivers
destinationsID = None



def read_parameters(args):
  global mqtt_data
  global node_data
  global log_file_location
  global local_COUNTRY

  with open(args.mqtt_file) as data:    
    mqtt_data = json.load(data)
    logging.debug(json.dumps(mqtt_data,indent=2))

  with open(args.node_id_file) as data:    
    node_data = json.load(data)
    logging.debug(json.dumps(node_data,indent=2))

  log_file_location=str(args.log_file)
  logging.debug("Log filename is: "+log_file_location)

  local_COUNTRY=str(args.local_country)
  logging.debug("Receiving code: "+local_COUNTRY)



##
##
"""
{
  "COUNTRY": "PRT",
  "ORGANISATION": "PARTICLE",
  "node_id": "PRT-S003",
  "assetType": "soldier",
  "assetName": "Gama",
  "functions": [
    "info",
    "location"
  ],
  "symbolCode": "SFGPUCA---"
}
"""

def write_log(msg_JSON, topic):
  global log_file_location
  global local_COUNTRY
  
  timestamp = datetime.now().astimezone().isoformat()

  #print(json.dumps(msg_JSON, indent=2))

  print('.', end='', flush=True)

  # check if contains 'properties' otherwise fill with None
  message_id = None
  sourceSystemID = None
  sourceTimestamp = 0
  coordinates = [ 0, 0, 0 ]
  if 'properties' in msg_JSON:
    if 'msg_id' in msg_JSON['properties']:
      message_id = msg_JSON['properties']['msg_id']
    if 'node_id' in msg_JSON['properties']:
      sourceSystemID = msg_JSON['properties']['node_id']
    if 'timestamp' in msg_JSON['properties']:
      sourceTimestamp = msg_JSON['properties']['timestamp']
  if 'geometry' in msg_JSON:
    if 'coordinates' in msg_JSON['geometry']:
      coordinates = msg_JSON['geometry']['coordinates']

  fw = open(log_file_location, "a+")

    # "DEU/FKIE/vehicle/100014/image/50000"

  msg_country = topic[0:3]
  msg_destinationSystemIDs = ['DEU', 'PRT', 'SGP', 'USA', 'NOR', 'POL']
  msg_destinationSystemIDs.remove(msg_country)

  if "/location" in topic :
    logMessageLog_JSON = {
        "positionMessageLog": {
          "loggingSystemID": node_data['node_id'],
          "loggingEventType": "sent" if topic.startswith(local_COUNTRY+"/") else "received",
          "messageID": message_id,
          "timestamp": timestamp,
          "sourceSystemID": msg_country,
          "destinationSystemIDs": msg_destinationSystemIDs,
          "positions": [
            {
              "systemID":  sourceSystemID,
              "timestamp": sourceTimestamp,
              "latitude":  coordinates[0],
              "longitude": coordinates[1]
             # "altitude":  coordinates[2]
            },
          ], # ,
          "raw_message": topic
        }
      }
    fw.write(json.dumps(logMessageLog_JSON, indent=2))
    fw.write("\n")
  else:    
    logMessageLog_JSON = {
      "textMessageLog": {
        "loggingSystemID": node_data['node_id'],
        "loggingEventType": "sent" if topic.startswith(local_COUNTRY+"/") else "received",
        "messageID": message_id,
        "timestamp": timestamp,
        "sourceSystemID": msg_country,
        "destinationSystemIDs": msg_destinationSystemIDs,
        "subject": topic,
        "text": ""
        # "raw_message": msg_JSON
      }
    }
    fw.write(json.dumps(logMessageLog_JSON, indent=2))
    fw.write("\n")
  #
  # log_PositionLog_JSON = {
  #   "positionLog": {
  #     "loggingSystemID": node_data['node_id'],
  #     "systemID": node_data['node_id'],
  #     "timestamp": timestamp,
  #     "latitude": coordinates[0],
  #     "longitude": coordinates[1],
  #     "altitude": coordinates[2]
  #  }
  # }
  # fw.write(json.dumps(log_PositionLog_JSON, indent=2))
  # fw.write("\n")
  #
  fw.close()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  global node_data
  logging.debug("Connected with result code "+str(rc))

  for topic in node_data['topics']:
    logging.debug("--subs to topic: " + topic)
    client.subscribe(topic)
    #client.subscribe(topic, qos=1)

#
def on_subscribe(client, userdata, mid, granted_qos):
  logging.debug(" subscribed: "+str(mid)+" "+str(granted_qos))
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  write_log(json.loads(msg.payload), msg.topic)
  

##########
## MAIN 

parser = argparse.ArgumentParser(
  description='Node subscriber.  Subscribed from topics and produces logs according to FKIE format.',
  epilog='This node will subscribe to all MQTT topics under the main topic (specified in the MQTT log file)',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('--country',
                    dest='local_country',
                    required=True,
                    help='Country code of the subscriber (e.g., DEU, NOR, POL, PRT, USA)')
parser.add_argument('--node',
                    dest='node_id_file', 
                    required=True,
                    help='File containing information concerning the node (e.g., node_id)')
parser.add_argument('--mqtt',
                    dest='mqtt_file', 
                    required=True,
                    help='File containing the parameters to connect to a MQTT server')
parser.add_argument('--log', 
                    dest='log_file', 
                    required=True,
                    help='Name of file to store log data')


args = parser.parse_args()
read_parameters(args)

print ("Write log in ",log_file_location)
fw = open(log_file_location, "w+")
fw.close()

client = mqtt.Client(node_data['node_id'])
#client.on_publish = on_publish
client.on_connect = on_connect
client.connect(mqtt_data['mqtt_ip'],mqtt_data['mqtt_port'],mqtt_data['mqtt_keepalive'])
client.on_subscribe = on_subscribe
client.on_message = on_message

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
