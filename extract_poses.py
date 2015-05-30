# extract_poses.py
# Dylan Auty 29/5/15
#
# Uses the Blender API to automatically extract the keyframes corresponding to various poses - can output them as JSON or CSV
# Aims to save time rather than manually exporting all values...

import bpy

action = bpy.data.actions['ColdBake']
for fc in action.fcurves:
    print(str(fc.data_path) + " channel " + str(fc.array_index))
    for keyframe in fc.keyframe_points:
        print(str(keyframe.co))
