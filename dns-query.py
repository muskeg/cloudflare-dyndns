#!/usr/bin/python

#*************************************************************************
#  Cloudflare DNS Query
#  
#  This script uses the Cloudflare's DNS API to query records on
#  your Cloudflare account and updates your cloudflare.config file
#  with the chosen A Record.
#
#**************************************************************************


import sys
if sys.version_info[0] == 2:
    from ConfigParser import RawConfigParser
if sys.version_info[0] >= 3:
    from configparser import RawConfigParser
import json
import requests


# read configuration file
config_file_name = sys.argv[1] or "cloudflare.config"
config = RawConfigParser()
config.read(config_file_name)

# Parse parameters
# Cloudflare
zone_id = config.get("cloudflare", "zone_id")
email = config.get("cloudflare", "email")
token = config.get("cloudflare", "global_token")

# Prepare GET request
cloudflare = "https://api.cloudflare.com/client/v4/zones/" + zone_id
api = "/dns_records/"
headers = {'Content-type': 'application/json', 'X-Auth-Email': email, 'X-Auth-Key': token}

# Get result for logging
r = requests.get(cloudflare + api, headers=headers)
query = json.loads(r.content)

if (query['success']):
    print("Query completed sucessfully");
    print("Records:");
    print("---------------------------------");

count = 0
# Print records
for record  in query['result']:
    count = count + 1
    print("{count}) {record_type} Record: {name} - ID: {record_id}".format(count = count, record_type = record['type'], name = record['name'], record_id = record['id']))

# Which record to update
if (count > 0):
    user_selected = 0
    while user_selected < 1 or user_selected > count:
        try:
            if sys.version_info[0] == 2:
                user_selected = int(raw_input("Please select a record: "))
            if sys.version_info[0] >= 3:
                user_selected = int(input("Please select a record: "))
        except ValueError:
            print("Please select a valid record..\n")
    
    choice = user_selected - 1
    print("Updating config file:")
    print("record_id = " + query['result'][choice]['id'])
    print("record_name = " + query['result'][choice]['name'])

    # Write record's name and ID to configuration file
    config.set("record", "record_id", query['result'][choice]['id'])
    config.set("record", "record_name", query['result'][choice]['name'])
    config_file = open(config_file_name, "w")
    config.write(config_file)
    config_file.close()

