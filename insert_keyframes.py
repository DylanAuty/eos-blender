# insert_keyframes.py
# Dylan Auty, 3/6/15
# Script to take data already extracted from the server as a JSON, select appropriate keyframes, and, um, insert them.

import json
import bpy
import datetime
from math import *

# Input stage
keyframeFile = open(bpy.path.abspath("//eos-blender/keyframesRaw.json"), 'r')
keyframeData = json.loads(keyframeFile.read())

# keyframeData contains 100 frames of pre-baked animation data for each F-Curve
# Each F-Curve is addressable by its data_path

telemetryFile = open(bpy.path.abspath("//eos-blender/testData.json"), 'r')
telemetryData = json.loads(telemetryFile.read())

length = len(telemetryData['d'])	# Should contain number of frames of data in the telemetry json
					# Also the number of keyframes we'll insert and modify for each f-curve
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

for i in range(0, length - 1):	# Iterate over every telemetry data snapshot
	print(i)
	currTemp = float(telemetryData['d'][i]['externaltemp'])
	# On first frame, grab timestamp and save it as the "start"
	print("Temp : " + str(currTemp))
	if(i == 0):
		startTime = float(telemetryData['d'][0]['timestamp'])

	# Select requisite frame from animation and determine where to insert keyframe
	currTime = float(telemetryData['d'][i]['timestamp'])
	frameNo = floor((currTime - startTime)/msPerFrame)	# frameNo should hopefully be a float at this point
	insertFrame = floor((tempUpperBound - currTemp) / degPerFrame) # frame 0 is normal, frame 99 is freezing
	if (insertFrame > 99.0):
		insertFrame = 99.0
	if (insertFrame < 0.0):
		insertFrame = 0.0

	for fc in action.fcurves:
		# FOR EACH F CURVE:
		# Insert a new keyframes
		# Edit it to fit with the data
		# Can do this using fc.keyframe_points[n].co.y = value (i.e. assigning keyframe values)
		# NB: frame is keyframe.co.x, value is keyframe.co.y
		#if (str(float(fc.array_index)) in keyframeData[str(fc.data_path)]):
		print("Inserting keyframes to: " + str(fc.data_path) + ", ch. " + str(fc.array_index))
		propString = str(fc.data_path).split('.')[-1]
		print('propString : ' + propString)
		#fc.keyframe_insert(propString, index=fc.array_index)
		# OR
		if(str(fc.array_index) in keyframeData[str(fc.data_path)]):
			fc.keyframe_points.add(1)	# THis may just...work
			fc.keyframe_points[i].co = (frameNo, keyframeData[str(fc.data_path)][str(fc.array_index)][int(insertFrame)][str(int(insertFrame))]['value'])	# God I'm ashamed of this line
		#fc.keyframe_points[i].co = (frameNo, i)
"""
May be able to add a keyframe to an fcurve using this:
class bpy.types.ActionFCurves(bpy_struct) is containiner for fcurves (as in action.fcurves)
action.fcurves.new(data_path, index, action_group) so can address fcurves using their data path
"""

telemetryFile.close()
keyframeFile.close()

