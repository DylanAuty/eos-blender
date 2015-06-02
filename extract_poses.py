# extract_poses.py
# Dylan Auty 29/5/15
#
# Uses the Blender API to automatically extract the keyframes corresponding to various poses - can output them as JSON or CSV
# Aims to save time rather than manually exporting all values...

import bpy
import json

action = bpy.data.actions['ColdBake Baked']
action2 = bpy.data.actions['PythonTest']

frameDict = {}

"""
for fc in action.fcurves:
	print(str(fc.data_path) + " channel " + str(fc.array_index))
	print("F-CURVE: " + str(fc)) #Does this mean anything?
	fc_index = fc.array_index
	fc_data_path = fc.data_path
	for keyframe in fc.keyframe_points:
		# print("KEYFRAME: " + str(keyframe)) # No idea if this'll do anything worthwhile
		# keyframe consists of a control point, left handle and right handle
		# their coordinates on the F-Curve graph can be accessed using .co, .handle_left, and .handle_right respectively
		print(str(keyframe.co.x) + ", " + str(keyframe.co.y))
		action2.fcurves[fc_data_path][fc_index].keyframe_points.insert(frame=keyframe.co.x, value=keyframe.co.y)
		
"""
frameCounter = 0

for fc in action.fcurves:
	print(str(fc.data_path) + " channel " + str(fc.array_index))
	for keyframe in fc.keyframe_points:
		frameDict[keyframe.co.x] = {
				'frameNo' : keyframe.co.x,
				'honhonhon' : 'baguette'}
	

print (json.dumps(frameDict, sort_keys=True, indent=4))
