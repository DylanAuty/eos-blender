# extract_poses.py
# Dylan Auty 29/5/15
#
# Uses the Blender API to automatically extract the keyframes corresponding to various poses - can output them as JSON or CSV
# Aims to save time rather than manually exporting all values...

import bpy

action = bpy.data.actions['CubeAction']
for fc in action.fcurves:
    if fc.data_path == 'location' and fc.array_index == 0:
        break

