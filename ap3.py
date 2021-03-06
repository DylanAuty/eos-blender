# ap3.py
# Dylan Auty, 9/6/15
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
colourFile = open(bpy.path.abspath("//eos-blender/colourData.json"), 'r')
colourData = json.loads(colourFile.read())

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

altLowerBound = 0.0
altUpperBound = 30000.0	# Altitude colour changing tops out at 30km
altRange = altUpperBound - altLowerBound

originalType = bpy.context.area.type	# To put the display back how it was at the end of the script

skinCol = [[[0 for x in range(4)] for x in range(2)] for x in range(2)]
bgCol = [[[0 for x in range(3)] for x in range(2)] for x in range(2)]	# Multidimensional lists need instantiation in Python

# Extract colours into arrays now, save doing it later
# SKIN:
# Start, elem0
skinCol[0][0][0] = float(colourData['colours']['start']['elem0']['R'])
skinCol[0][0][1] = float(colourData['colours']['start']['elem0']['G'])	# Indices are, in order: [start/end][element no.][RGBA selection]
skinCol[0][0][2] = float(colourData['colours']['start']['elem0']['B'])
skinCol[0][0][3] = float(colourData['colours']['start']['elem0']['A'])
# Start, elem1
skinCol[0][1][0] = float(colourData['colours']['start']['elem1']['R'])
skinCol[0][1][1] = float(colourData['colours']['start']['elem1']['G'])	
skinCol[0][1][2] = float(colourData['colours']['start']['elem1']['B'])
skinCol[0][1][3] = float(colourData['colours']['start']['elem1']['A'])
# Finish, elem0
skinCol[1][0][0] = float(colourData['colours']['finish']['elem0']['R'])
skinCol[1][0][1] = float(colourData['colours']['finish']['elem0']['G'])
skinCol[1][0][2] = float(colourData['colours']['finish']['elem0']['B'])
skinCol[1][0][3] = float(colourData['colours']['finish']['elem0']['A'])
# Finish, elem1
skinCol[1][1][0] = float(colourData['colours']['finish']['elem1']['R'])
skinCol[1][1][1] = float(colourData['colours']['finish']['elem1']['G'])
skinCol[1][1][2] = float(colourData['colours']['finish']['elem1']['B'])
skinCol[1][1][3] = float(colourData['colours']['finish']['elem1']['A'])

# BACKGROUND - Only RGB, no alpha channel
# Start, horizon colour
bgCol[0][0][0] = float(colourData['colours']['start']['hcol']['R'])
bgCol[0][0][1] = float(colourData['colours']['start']['hcol']['G'])
bgCol[0][0][2] = float(colourData['colours']['start']['hcol']['B'])
# Start, zenith colour
bgCol[0][1][0] = float(colourData['colours']['start']['zcol']['R'])
bgCol[0][1][1] = float(colourData['colours']['start']['zcol']['G'])
bgCol[0][1][2] = float(colourData['colours']['start']['zcol']['B'])
# Finish, horizon colour
bgCol[1][0][0] = float(colourData['colours']['finish']['hcol']['R'])
bgCol[1][0][1] = float(colourData['colours']['finish']['hcol']['G'])
bgCol[1][0][2] = float(colourData['colours']['finish']['hcol']['B'])
# Finish, zenith colour
bgCol[1][1][0] = float(colourData['colours']['finish']['zcol']['R'])
bgCol[1][1][1] = float(colourData['colours']['finish']['zcol']['G'])
bgCol[1][1][2] = float(colourData['colours']['finish']['zcol']['B'])


for i in range(0, length - 1):	# Iterate over snapshots of data
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

	bpy.context.area.type = "DOPESHEET_EDITOR"
	for s in bpy.context.area.spaces:
		if s.type == "DOPESHEET_EDITOR":
			s.mode = "ACTION"
			s.action = bpy.data.actions.get("ColdBake Baked") # Switch to dopesheet editor in action mode, switch current action to whatever	
	bpy.data.scenes["Scene"].frame_set(int(insertFrame))	# Change current frame of the animation
	# Now swap context to 3d view, copy armature pose
	bpy.context.area.type = "VIEW_3D"
	bpy.ops.pose.copy()
	# Swap back to dopesheet editor, switch action, change frame, switch to 3d view, paste pose
	bpy.context.area.type = "DOPESHEET_EDITOR"
	for s in bpy.context.area.spaces:
		if s.type == "DOPESHEET_EDITOR":
			s.mode = "ACTION"
			s.action = bpy.data.actions.get("PythonTest")
	bpy.data.scenes["Scene"].frame_set(int(frameNo))
	bpy.context.area.type = "VIEW_3D"
	bpy.ops.pose.paste(flipped=False)	# This should hopefully auto-insert a keyframe...
	
	# Pose is done, so now change colour of the skin and hope it keyframes it...
	# 2 elements in the colour ramp (for toon shadint) - elem0 first
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].color[0] = (((skinCol[1][0][0] - skinCol[0][0][0])/bakedFrameNo) * insertFrame) + skinCol[0][0][0]
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].color[1] = (((skinCol[1][0][1] - skinCol[0][0][1])/bakedFrameNo) * insertFrame) + skinCol[0][0][1]
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].color[2] = (((skinCol[1][0][2] - skinCol[0][0][2])/bakedFrameNo) * insertFrame) + skinCol[0][0][2]
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].color[3] = (((skinCol[1][0][3] - skinCol[0][0][3])/bakedFrameNo) * insertFrame) + skinCol[0][0][3]
	# Now elem1
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].color[0] = (((skinCol[1][1][0] - skinCol[0][1][0])/bakedFrameNo) * insertFrame) + skinCol[0][1][0]
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].color[1] = (((skinCol[1][1][1] - skinCol[0][1][1])/bakedFrameNo) * insertFrame) + skinCol[0][1][1]
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].color[2] = (((skinCol[1][1][2] - skinCol[0][1][2])/bakedFrameNo) * insertFrame) + skinCol[0][1][2]
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].color[3] = (((skinCol[1][1][3] - skinCol[0][1][3])/bakedFrameNo) * insertFrame) + skinCol[0][1][3]
	# Also do the background colour - horizon colour and zenith to be set
	# Horizon colour
	bpy.data.worlds["World"].horizon_color[0] = (((bgCol[1][0][0] - bgCol[0][0][0])/altRange) * float(telemetryData['d'][i]['altitude'])) + bgCol[0][0][0]
	bpy.data.worlds["World"].horizon_color[1] = (((bgCol[1][0][1] - bgCol[0][0][1])/altRange) * float(telemetryData['d'][i]['altitude'])) + bgCol[0][0][1]
	bpy.data.worlds["World"].horizon_color[2] = (((bgCol[1][0][2] - bgCol[0][0][2])/altRange) * float(telemetryData['d'][i]['altitude'])) + bgCol[0][0][2]
	# Zenith colour
	bpy.data.worlds["World"].zenith_color[0] = (((bgCol[1][1][0] - bgCol[0][1][0])/altRange) * float(telemetryData['d'][i]['altitude'])) + bgCol[0][1][0]
	bpy.data.worlds["World"].zenith_color[1] = (((bgCol[1][1][1] - bgCol[0][1][1])/altRange) * float(telemetryData['d'][i]['altitude'])) + bgCol[0][1][1]
	bpy.data.worlds["World"].zenith_color[2] = (((bgCol[1][1][2] - bgCol[0][1][2])/altRange) * float(telemetryData['d'][i]['altitude'])) + bgCol[0][1][2]

	# KEYFRAME ALL THE THINGS
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].keyframe_insert(data_path="color", frame=frameNo, index=0)
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].keyframe_insert(data_path="color", frame=frameNo, index=1)
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].keyframe_insert(data_path="color", frame=frameNo, index=2)
	bpy.data.materials["Skin"].diffuse_ramp.elements[0].keyframe_insert(data_path="color", frame=frameNo, index=3)
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].keyframe_insert(data_path="color", frame=frameNo, index=0)
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].keyframe_insert(data_path="color", frame=frameNo, index=1)
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].keyframe_insert(data_path="color", frame=frameNo, index=2)
	bpy.data.materials["Skin"].diffuse_ramp.elements[1].keyframe_insert(data_path="color", frame=frameNo, index=3)
	bpy.data.worlds["World"].keyframe_insert(data_path="horizon_color", frame=frameNo, index=0)
	bpy.data.worlds["World"].keyframe_insert(data_path="horizon_color", frame=frameNo, index=1)
	bpy.data.worlds["World"].keyframe_insert(data_path="horizon_color", frame=frameNo, index=2)
	bpy.data.worlds["World"].keyframe_insert(data_path="zenith_color", frame=frameNo, index=0)
	bpy.data.worlds["World"].keyframe_insert(data_path="zenith_color", frame=frameNo, index=1)
	bpy.data.worlds["World"].keyframe_insert(data_path="zenith_color", frame=frameNo, index=2)
	
bpy.context.area.type = originalType

telemetryFile.close()
keyframeFile.close()
colourFile.close()

