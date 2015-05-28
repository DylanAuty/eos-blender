# db_data_pull.py
# Dylan Auty, 28/5/15
# 
# Purpose of script is to pull all raw data necessary from the
# Cloudant database hosted in Bluemix, and maybe do some preliminary processing of it
# 
# Part of application to transform raw telemetry data from balloon into CSV describing
# F-Curves for every relevant bit of the Blender scene.

import json
from datetime import datetime
import time
import logging
import requests

# First import the settings file and parse it as a dict
# Kept separate because of modularity and security

settingsFile = open('./settings.json', 'r+')
settings = json.loads(settingsFile.read())

API_KEY = settings['settings']['API_KEY']
PASSWORD = settings['settings']['PASSWORD'] # I.. don't know why these are in caps
get_url = settings['settings']['GET_URL']

# Authenticate with the Bluemix API
r = requests.Session()
r.auth = (API_KEY, PASSWORD)

# Construct the payload and attempt the HTTP GET
payload = {'WHO KNOWS': 'BLAHBLAH'}

try:
    reply = r.get(get_url, verify=False, params=payload)

except requests.exceptions.RequestException as e:
    # Can do stuff with str(e) if I want.. I don't really, though
    # temp. soln.: retry 10 times, then exit
    y = 1 
    retrySucceed = False
    for y in range(1, 10):
        try:
            reply = r.get(get_url, verify=False, params=payload)
        except requests.exceptions.RequestException as e1:
            pass    # This would be a good place for logging to be done
        else:
            retrySucceed = True
            break   # Retry succeeded
    if not retrySucceed:
        print "ERROR: Retry failed"
        
# Output stage
output = open("./HRRRM/PLACEHOLDER.json", 'w')
output.write(str(reply.content))
output.close()

settingsFile.close()
