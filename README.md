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

### Comparing these two approaches, I will be proceeding with approach 2.

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


