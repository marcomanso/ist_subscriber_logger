import argparse
from datetime import datetime

import json
import dirtyjson

# main key: textMessageLog

# read once:  loggingSystemID

# sourceSystemID

# subject ?

logging_system = None
logging_system_date = None

logging_data_received = {}
logging_data_sent = {}


def print_data(data_map):
    keys = sorted(data_map.keys())
    for key in keys:
        print( "%s\t%d" % (key, data_map[key]) )

    #for key in data_map:
    #    print( "%s\t%d" % (key, data_map[key]) )
        #print("key=", key, " value=", data_map[key])



parser = argparse.ArgumentParser(
  description='Log analyser.  Extracts some basic measurements from log.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('--input',
                    dest='input_file',
                    required=True,
                    help='Input log file')


args = parser.parse_args()

input_file = args.input_file
print ("Processing log ",input_file)

file = open(input_file, 'r')
#data_jsonfile = json.load(file)
data_jsonfile = dirtyjson.load(file)

for json_element in data_jsonfile:

    log_element = None
    if "textMessageLog" in json_element:
        log_element = json_element["textMessageLog"]
    elif "positionMessageLog" in json_element:
        log_element = json_element["positionMessageLog"]
    else:
        print("unknown type for:", json_element)

    if log_element is not None:
        if logging_system is None:
            logging_system = log_element["loggingSystemID"]
        if logging_system_date is None:
            logging_system_date = log_element["timestamp_ISO"]
        if log_element["loggingEventType"] == "received":
            #print(">", end="")
            if log_element["sourceSystemID"] not in logging_data_received:
                logging_data_received[log_element["sourceSystemID"]] = 0
            logging_data_received[log_element["sourceSystemID"]] = logging_data_received[log_element["sourceSystemID"]]+1
        if log_element["loggingEventType"] == "sent":
            #print("<", end="")
            if log_element["sourceSystemID"] not in logging_data_sent:
                logging_data_sent[log_element["sourceSystemID"]] = 0
            logging_data_sent[log_element["sourceSystemID"]] = logging_data_sent[log_element["sourceSystemID"]]+1


print("done!")
print("Log file:", input_file)
print("Logging system:", logging_system)
print("-- first time:", logging_system_date)
print("-- sent:")
print(print_data(logging_data_sent))
print("-- received:")
print_data(logging_data_received)
