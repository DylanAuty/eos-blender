# extract_poses.py
# Dylan Auty 29/5/15
#
# Uses the Blender API to automatically extract the keyframes corresponding to various poses - can output them as JSON or CSV
# Aims to save time rather than manually exporting all values...

import bpy

action = bpy.data.actions['ColdBake']
for fc in action.fcurves:
    print(fc.data_path + " channel " + fc.array_index)
    for keyframe in keyframe_points:
        print("COORDINATES: " + keyframe.co)
