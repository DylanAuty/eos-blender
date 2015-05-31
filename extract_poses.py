# extract_poses.py
# Dylan Auty 29/5/15
#
# Uses the Blender API to automatically extract the keyframes corresponding to various poses - can output them as JSON or CSV
# Aims to save time rather than manually exporting all values...

import bpy
import json

action = bpy.data.actions['ColdBake']
for fc in action.fcurves:
	print(str(fc.data_path) + " channel " + str(fc.array_index))
	print("F-CURVE: " + str(fc)) #Does this mean anything?
	for keyframe in fc.keyframe_points:
		print("KEYFRAME: " + str(keyframe)) # No idea if this'll do anything worthwhile
		# keyframe consists of a control point, left handle and right handle
		# their coordinates on the F-Curve graph can be accessed using .co, .handle_left, and .handle_right respectively
		print(str(keyframe.co.x) + ", " + str(keyframe.co.y))

print ("DONE PRINTING...")

action2 = bpy.data.actions['PythonTest']	# Gonna try and insert a keyframe everywhere, value 5, frame 200
for fc in action2.fcurves:
	print(str(fc.data_path) + " channel " + str(fc.array_index))
	# First insert a keyframe for everything at the start...
	fc.keyframe_points.insert(frame=200, value=2, options={'REPLACE'})
	# Now print out all keyframes...
	for keyframe in fc.keyframe_points:
		print("KEYFRAME: " + str(keyframe))
		print(str(keyframe.co.x) + ", " + str(keyframe.co.y))
