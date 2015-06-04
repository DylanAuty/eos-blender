# insert_keyframes.py
# Dylan Auty, 3/6/15
# Script to take data already extracted from the server as a JSON, select appropriate keyframes, and, um, insert them.

import json
import bpy
import datetime
from math import *

# Input stage
keyframeFile = open("keyframesRaw.json", 'r')
keyframeData = json.loads(keyframeFile.read())

# keyframeData contains 100 frames of pre-baked animation data for each F-Curve
# Each F-Curve is addressable by its data_path

telemetryFile = open("telemetry.json", 'r')
telemetryData = json.loads(telemetryFile.read())

length = len(telemetryData['d'])	# Should contain number of frames of data in the telemetry json
print ("length = " + str(length))
action = bpy.data.actions['PythonTest']

startTime = 0 # Initialise startTime to 0 (formatted as milliseconds since epoch, Date.now() in JS)
frameNo = 0.0 # contains the frame into which the prebaked animation must be inserted
insertFrame = 0.0 # contains the frame from the prebaked animation to be inserted into frameNo of animation
frameRate = 24 # To calculate which frame to insert a particular snapshot of data into
msPerFrame = 1000/frameRate
bakedFrameNo = 100 # No. of frames in pre-made animation - allows changing at a later stage

tempLowerBound = -50.0
tempUpperBound = 24.0	# Setting "normal" and "cold" points
tempRange = tempUpperBound - tempLowerBound
degPerFrame  = tempRange/bakedFrameNo # How many degrees of real temperature correspond to each frame of baked animation

for i in (0, length):	# Iterate over every telemetry data snapshot
	currTemp = telemetryData['d'][i]['temperature']
	# On first frame, grab timestamp and save it as the "start"
	if(i == 0):
		startTime = telemetryData['d'][0]['timestamp']

	# Select requisite frame from animation and determine where to insert keyframe
	currTime = telemetryData['d'][i]['timestamp']
	frameNo = floor((currTime - startTime)/msPerFrame)	# frameNo should hopefully be a float at this point
	insertFrame = floor((tempUpperBound - currTemp) / degPerFrame) # frame 0 is normal, frame 99 is freezing
	if (insertFrame > 99.0):
		insertFrame = 99.0
	if (insertFrame < 0.0):
		insertFrame = 0.0

	for fc in action.fcurves:
		print("Inserting keyframe to: " + str(fc.data_path) + ", ch. " + str(fc.array_index))
		print("Frame " + str(keyframeData[str(insertFrame)]))
		fc.insert(frame=frameNo, value=keyframeData[str(fc.data_path)][str(insertFrame)]['value'])
		#action.fcurves.new(data_path=fc.data_path
		#action2.fcurves[fc_data_path][fc_index].keyframe_points.insert(frame=keyframe.co.x, value=keyframe.co.y)
	

"""
May be able to add a keyframe to an fcurve using this:
class bpy.types.ActionFCurves(bpy_struct) is containiner for fcurves (as in action.fcurves)
action.fcurves.new(data_path, index, action_group) so can address fcurves using their data path
"""

#telemetryFile.close()
keyframeFile.close()

