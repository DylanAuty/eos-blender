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
tempList = []

for fc in action.fcurves:
	print("Data Path: " + str(fc.data_path) + " array index : " + str(fc.array_index) + " group : " + str(fc.group))
	frameDict[str(fc.data_path)] = {}
	
	for keyframe in fc.keyframe_points:
		tempList.append({str(int(keyframe.co.x)) : {
			'frame' : int(keyframe.co.x),
			'value' : keyframe.co.y
			}
		}
		)
	
	frameDict[str(fc.data_path)][str(fc.array_index)] = tempList
	tempList = []

# Output stage
print ("Saving to: " + str(bpy.path.abspath("//eos-blender/keyframesRaw.json")))

output = open(bpy.path.abspath("//eos-blender/keyframesRaw.json"), 'w')
output.write(json.dumps(frameDict, indent=4, sort_keys=True))
output.close()


