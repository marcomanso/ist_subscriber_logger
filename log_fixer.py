import argparse
import json
import os
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


def millis_to_iso(millis):
    return str(datetime.fromtimestamp(float(millis))) + "+00:00"

def get_valid_data(data, nopol):

    try:
        data_content = None
        
        if ("textMessageLog" in data):
            data_content = data.get("textMessageLog")
            if(nopol and data_content["sourceSystemID"] == "POL"):
                return None
            
        elif ("positionMessageLog" in data):
            data_content = data.get("positionMessageLog")
            if(nopol and data_content["sourceSystemID"] == "POL"):
                return None
            
            positions = data_content["positions"][0]
            if(positions["timestamp"] == "0" and positions["timestamp_ISO"] is not None):
                 iso = positions["timestamp_ISO"]
                 fixed=False
                 
                 #fix errors in us logs
                                  
                 #1. fix custom format error (spaces, no "T", extra digits)
                 if(" " in iso): # error 1 can be identified by spaces
                    #fixed=True
                    iso = iso[:10] + "T" + iso[11:] # insert missing "T"
                    iso_offset = iso[30:]                 
                    iso = iso[:26] # cuts off extra digits after 6 that break ISO format
                    if(iso_offset=="+0000 UTC" or iso_offset=="0000 UTC"):
                        iso = iso + "+00:00" # use ISO offset format instead of custom
                    elif(iso_offset=="-0400 EDT"): 
                        iso = iso + "-04:00" # use ISO offset format instead of custom
                    else: 
                        print("\n+++++++++ ERROR +++++++++\n")
                        return None                    
                    positions["timestamp_ISO"] = iso # write back corrected format
                    #fixed=True
                   
                 #2. fix custom format error (format "seconds")
                 elif("seconds:" in iso):
                    iso = iso[8:] # prelim. fix, converter should be able to handle this 
                    positions["timestamp_ISO"] = millis_to_iso(int(iso))
                    return None # discard - could be fixed but probably can't be used due to time resolution (only seconds, need milliseconds)
                    
                 #3. fix custom format error (missing digits)
                 elif(len(iso) < 26):
                    iso = iso[:19] + ".000000" + iso[19:] # insert missing digits
                    positions["timestamp_ISO"] = iso # write back corrected format
                    return None # discard - could be fixed but probably can't be used due to time resolution (only seconds, need milliseconds)
                    
                 positions["timestamp"] = to_unix_time_millis(iso)          
                 if(fixed): print("\nfixed " +iso+" = " + str(positions["timestamp"]) + "")
                
        else:
            return None

        #remove non participating nations
        if("destinationSystemIDs" in data_content):
            if(nopol): data_content["destinationSystemIDs"].remove("POL")
            data_content["destinationSystemIDs"].remove("SGP")

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


# print(to_unix_time_millis("2023-08-18T08:47:05-06:00"))
# exit(0)

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
parser.add_argument('--nopol',
                    dest='nopol',
                    required=False,
                    help='Remove Poland entries (set to 1)')

args = parser.parse_args()

input_file = args.input_file
nopol = (args.nopol != None) and args.nopol == "1"

print ("Processing log ",input_file)

data_raw = open(input_file, 'r')
data_as_array = open(get_filename_array(input_file), 'w')
data_as_array.write("[\n")
for data in data_raw:
    d = data
    if(d=="}\n"): d="},\n"
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
    data_valid = get_valid_data(data, nopol)
    if data_valid is not None:
        json_data_valid_array.append(data_valid)
        print("+",end="")
    else:
        print("-",end="")


# save in file
output_file=args.output_file
print ("Writing to ",output_file, end="")
data_output = open(output_file, "w")
for json_data in json_data_valid_array:
    data_output.write(json.dumps(json_data, indent=2))
    data_output.write("\n")
data_output.close()

os.remove(get_filename_array(input_file))

print (".. done.  Bye !")
