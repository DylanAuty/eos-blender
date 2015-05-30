# json_to_fcurve.py
# Dylan Auty, 29/5/15
# 
# Converts JSON received from server into F-Curves, formatted as CSV
# Format of every CSV is {frame, value}, where value varies depending on which F-Curve the CSV is for
#
# INPUT: 
#   - CSV files detailing each pose - 10 per bone for location (3), rotation (4) and scaling (3)
#   - JSON file containing all data, one object containing sub-objects for each frame of data
# OUTPUT:
#   - A stupid quantity of CSV files, 10 per bone for pose plus 3 for colours of the skin

import json
from datetime import datetime
import time

# Import the data as a dict and count the frames of data
telDataFile = open('./telemetry.json', 'r+')
telData = json.loads(telDataFile.read())
frameNum = len(telData['d'])    # !!!top level entity name uncertain yet!!!

# Aim now is to extract data, convert it into something meaningful and export the appropriate frame of the pre-baked animation...


