# eos-blender
Part of university group project, scripts relating to Blender animation and F-Curve import for automated animation from the raw JSON data.

## Overview
This repository is part of a university group project that aims to send a meteorological balloon into the stratosphere, beam the telemetry data it collects back to Earth, and then display the data in a meaningful way. To this end, we have a website, which you can visit [here](eos.mybluemix.com). It will contain both a live tracker, and an animation that will be rendered using the data after the launch. This repository contains scripts relating to the import of the information into Blender, the 3D modelling program being used to create the animation.

## Function and Purpose
An F-Curve is a Bezier curve, and every control point on the curve is called a Keyframe. When animating, you can use an F-Curve to describe the way in which a particular property of a model changes over time - anything from position in 3D space of a particular bit of the figure, to the colour of the material that makes up the shirt he wears. In this case, the challenge is to use real data to create F-Curves that will represent the data in a meaningful way. 

### Approach 1 - Interpolation between poses
There is a tool that allows for the import of CSV files containing data into Blender as an F-Curve, which you can find [here](http://blenderartists.org/forum/showthread.php?209181-A-Script-to-Import-a-CSV-File-and-Create-F-Curves-%28for-Blender-2-5x-or-later%29). However, in a model there may be hundreds of F-Curves to completely describe the scene.

I aim to take our incoming data, which is formatted as a JSON showing a snapshot of the telemetry at a given time, and break it into meaningful CSV files that can be easily imported into Blender as F-Curves. Once the program can reliably generate CSVs for each F-Curve, I will attempt to create a script that will use the [Blender Python API](http://www.blender.org/api/blender_python_api_2_74_5/) to automatically import the results, and generate the output. The ideal finished product would be able to do everything from extracting the raw data from the server, right up to initiating the final render.

### Approach 2 - Selecting and inserting pre-baked keyframes
It is also possible to use the Blender API to insert keyframes, rather than entire F-Curves. This can be useful, as pre-baking an F-Curve with an animation for a transition between two extremes allows a keyframe to be generated for every step along the scale. The major advantage of this is that no interpolation needs to be done outside of Blender, and the smooth Bezier interpolation done within Blender is preserved. Each keyframe is a point on an F-Curve described by a control point, a left handle and a right handle. These each have coordinates that can be exported - but it may not be necessary to export the control handles if the curves are pre-baked every frame (i.e. no interpolation information is necessary). This approach would select a keyframe according to incoming data, and insert it into the timeline to construct F-Curves.

### Approach 3 - Using the Blender API to simulate user input
In Blender, premade animations can be created called Actions. The Blender API is built in such a way that every function that the user can perform using the GUI can also be performed using a python script. This approach would be to build a python script that would simulate the following steps, assuming that an action already exists containing the premade hot-to-cold animation:
- Use telemetry data to work out which frame is required
- Switch to pre-baked action
- Switch to the requisite frame of the prebaked action
- Select the armature and switch to pose mode
- Copy the pose
- Switch to the output action
- Switch to the correct frame into which the pose should be inserted
- Select the armature and switch to pose mode
- Paste the pose (Copying and pasting poses is handled with a function in the Blender API)
- Select the skin and set the colours of the control points on the colour ramp (these need to be taken from a file because of the way actions work, they can't be stored as an action and are altered universally
- (This step may not be necessary) Insert a keyframe for the whole character (entire armature) at that frame (when doing this as a user, keyframes are inserted automatically)
- Repeat



## Approach selection
Having attempted to make the second approach work, I have found that despite saving all pose data using the *extract_poses.py* script, re-inserting them produced a garbage animation. To check this, I generated test data using *genData.py* which followed the JSON structure that the real data will have. I had it create 150 snapshots of data, varying the external temperature from -50 to 100 degrees C. In light of this failure, I believe the problem is to do with the way Blender handles posing - it is unclear from the documentation whether the values of the keyframes are relative or absolute. It is also unclear what the consequences are of attempting to pose a bone which is part of a rig (e.g. the foot roll rig, or the leg inverse kinematic rig) are, though it is possible that these are some sources of the problems.

I will be attempting approach 3. It removes a large layer of complexity that may not be needed (exporting and re-importing data), and certainly works when performed by a human. It remains to be seen whether the Python API is capable of accurately replicating the actions the user took.

## Files
### Scripts
- *db_data_pull.py*: Grabs a gigantic JSON containing telemetry data from the server, puts it in *telemetry.json*
- *extract_poses.py*: Script to extract the keyframes from the pre-baked F-Curve, and put them in a JSON
- *insert_keyframes.py*: Script to insert relevant keyframe into the live action based on data
- *README.md*: This file...
- *settings.json*: Contains various settings - GET URL, and if needed then API keys and passwords (though we don't have this at present)

### Input
*keyframesRaw.json*: JSON object pulled and formatted from F-Curves of a smooth animation, containing information on every keyframe in the pre-baked animation
*telemetry.json*: JSON object pulled from server containing all the launch data in sub-objects.

### Output
There are ~10 F-Curves per bone (depending on rotation type - 3 for Euler, 4 for Quaternion):
- X Location
- Y Location
- Z Location
- W Quaternion Rotation
- X Quaternion Rotation
- Y Quaternion Rotation
- Z Quaternion Rotation
- X Scale
- Y Scale
- Z Scale

=> >700 F-Curves, for each of which an appropriate keyframe will be inserted for every frame of incoming data.

Toon shading will be used, which demands 2 colours for the skin => 6 curves - Red, Blue and green for each colour. More may be used, but this is a lower priority than producing a functioning product.


