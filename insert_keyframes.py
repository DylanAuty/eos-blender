# insert_keyframes.py
# Dylan Auty, 3/6/15
# Script to take data already extracted from the server as a JSON, select appropriate keyframes, and, um, insert them.

import json

# Input stage
keyframeFile = open("keyframesRaw.json", 'r')
keyframeData = json.loads(keyframeFile.read())

# keyframeData contains 100 frames of pre-baked animation data for each F-Curve
# Each F-Curve is addressable by its data_path

#telemetryFile = open("telemetry.json", 'r')
#telemetryData - json.loads(telemetryFile.read())

length = len(keyframeData["pose.bones[\"Roll_back.L\"].scale"])
print ("length = " + str(length))
print (str(keyframeData["pose.bones[\"Roll_back.L\"].scale"]["data_path"]))

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
"""
May be able to add a keyframe to an fcurve using this:
class bpy.types.ActionFCurves(bpy_struct) is containiner for fcurves (as in action.fcurves)
action.fcurves.new(data_path, index, action_group) so can address fcurves using their data path
"""

#telemetryFile.close()
keyframeFile.close()

