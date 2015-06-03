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

for fc in action.fcurves:
	print(str(fc.data_path) + " channel " + str(fc.array_index))
	frameDict[str(fc.data_path)] = {'data_path' : fc.data_path}
	for keyframe in fc.keyframe_points:
		frameDict[str(fc.data_path)][keyframe.co.x] = {
				'frame' : keyframe.co.x,
				'value' : keyframe.co.y
				}

# Output stage
print ("Saving to: " + str(bpy.path.abspath("//eos-blender")))

output = open(bpy.path.abspath("//eos-blender/keyframesRaw.json"), 'w')
output.write(json.dumps(frameDict, indent=4))
output.close()


