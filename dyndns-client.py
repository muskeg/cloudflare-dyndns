#!/usr/bin/python

#*************************************************************************
#  Cloudflare Dynamic DNS Client
#  
#  This script uses the Cloudflare's DNS API to update an
#  existing (emphasis on existing) A Record to point to the local
#  public IP fetched from the ipify.org API.
#
#  Configuration is fetched from the clouflare.config file that should be
#  in the same folder as the script. 
#  Make sure to update it accordingly. 
#  Values can be found in the Cloudflare dashboard: https://dash.cloudflare.com/ 
#  under the API section, including links to API tokens sections of your profile.
#  The script is built to use the Global API Key for your account
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
config_file_name = "cloudflare.config"
config = RawConfigParser()
config.read(config_file_name)

# Parse parameters
# Cloudflare
try:
    zone_id = config.get("cloudflare", "zone_id")
    email = config.get("cloudflare", "email")
    token = config.get("cloudflare", "global_token")

# Record parameters
record_id = config.get("record", "record_id")
record_name = config.get("record", "record_name")
proxied = config.getboolean("record", "proxied")
ttl  = config.getboolean("record", "ttl")
# Simple request to get IP
ip = requests.get('https://api.ipify.org').text

# Prepare PUT request
cloudflare = "https://api.cloudflare.com/client/v4/zones/" + zone_id
api = "/dns_records/" + record_id
headers = {'Content-type': 'application/json', 'X-Auth-Email': email, 'X-Auth-Key': token}

data = {
    'type': 'A',
    'name': record_name,
    'content': ip,
    'proxied': proxied,
    'ttl': ttl
}

# Get result for logging
data_json = json.dumps(data)
r = requests.put(cloudflare + api, data=data_json, headers=headers)
result = json.loads(r.content)

print("Updating  {record_name} with ip: {ip} (result: {succes})".format(record_name = result['result']['name'], ip = result['result']['content'], success = str(result['success']))

