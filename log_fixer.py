import argparse
import json
import dirtyjson
from datetime import datetime

import traceback

import logging
logging.basicConfig(level=logging.DEBUG)


def get_filename_array(filename):
    return filename+"_dummytoremove"


## utils

def to_unix_time_millis(timestr):
  dt = None
  try:  # assume isoformat first
    dt = datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S.%f%z")
  except:
    try:  # if not, assume epoch seconds
      dt = datetime.fromtimestamp(float(timestr))
    except:
      try:  # if not, assume epoch milliseconds
        dt = datetime.fromtimestamp(float(timestr) / 1000.0)
      except:
        pass

  try:  # if dt=1/1/1970, timestamp throws an exception
    return round(dt.timestamp() * 1000.0) # round because analyzer expects a "long" here
  except:
    return None


def get_valid_data(data):

    try:
        data_content = None
        if ("textMessageLog" in data):
            data_content = data.get("textMessageLog")
        elif ("positionMessageLog" in data):
            data_content = data.get("positionMessageLog")
        else:
            return None

        #exclude info
        if ("subject" in data_content and data_content["subject"].endswith("/info")):
            return None

        #need to fix time?
        #if (data_content["timestamp_ISO"] is not None and data_content["timestamp"] is None):
        if (data_content["timestamp_ISO"] is not None):
                data_content["timestamp"] = to_unix_time_millis(data_content["timestamp_ISO"])

        # check if valid
        if (data_content["messageID"] is None or data_content["timestamp_ISO"] is None or data_content["timestamp"] is None):
            return None
        else:
            return data
    except Exception as err:
        #print(err)
        traceback.print_exc()
        return None


parser = argparse.ArgumentParser(
  description='Log fixer.  Performs some fixes in log files (like timestamp, remove messages without IDs, etc)',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('--input',
                    dest='input_file',
                    required=True,
                    help='Input log file')
parser.add_argument('--output',
                    dest='output_file',
                    required=True,
                    help='Output log file')


args = parser.parse_args()

input_file = args.input_file
print ("Processing log ",input_file)

data_raw = open(input_file, 'r')
data_as_array = open(get_filename_array(input_file), 'w')
data_as_array.write("[\n")
for data in data_raw:
    d = data.replace("}", "},")
    data_as_array.write(d)
data_as_array.write("\n]")
data_as_array.close()

print ("Processing post-log ", get_filename_array(input_file))
json_data_array=[]
with open(get_filename_array(input_file)) as data:

    #logging.debug(data)

    #json_data = demjson3.decode(data)
    #logging.debug(json_data)

    json_data_array = dirtyjson.load(data)
    #logging.debug(json_data)

    #node_data = json.load(data)
    #logging.debug(json.dumps(node_data, indent=2))

print("-- got # records: "+str(len(json_data_array)))

# filter only valid data
json_data_valid_array=[]
for data in json_data_array:
    data_valid = get_valid_data(data)
    if data_valid is not None:
        json_data_valid_array.append(data_valid)
        print("+",end="")
    else:
        print("-",end="")


# save in file
output_file=args.output_file
print ("Writing to ",output_file, end="")
data_output = open(output_file, "w")
data_output.write(json.dumps(json_data_valid_array))
data_output.close()

print (".. done.  Bye !")
