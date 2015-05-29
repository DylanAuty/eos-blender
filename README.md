# eos-blender
Part of university group project, scripts relating to Blender animation and F-Curve import for automated animation from the raw JSON data.

## Overview
This repository is part of a university group project that aims to send a meteorological balloon into the stratosphere, beam the telemetry data it collects back to Earth, and then display the data in a meaningful way. To this end, we have a website, which you can visit [here](eos.mybluemix.com). It will contain both a live tracker, and an animation that will be rendered using the data after the launch. This repository contains scripts relating to the import of the information into Blender, the 3D modelling program being used to create the animation.

## Function and Purpose
When animating, you can use an F-Curve to describe the way in which a particular property of a model changes over time - anything from position in 3D space of a particular bit of the figure, to the colour of the material that makes up the shirt he wears. In this case, the challenge is to use real data to create F-Curves that will represent the data in a meaningful way. 

There is a tool that allows for the import of CSV files containing data into Blender as an F-Curve, which you can find referenced [here](http://blenderartists.org/forum/showthread.php?209181-A-Script-to-Import-a-CSV-File-and-Create-F-Curves-%28for-Blender-2-5x-or-later%29). However, in a model there may be hundreds of F-Curves to completely describe the scene.

I aim to take our incoming data, which is formatted as a JSON showing a snapshot of the telemetry at a given time, and break it into meaningful CSV files that can be easily imported into Blender. Once the program can reliably generate CSVs for each F-Curve, I will attempt to create a script that will use the [Blender Python API](http://www.blender.org/api/blender_python_api_2_74_5/) to automatically import the results, and generate the output. The ideal finished product would be able to do everything from extracting the raw data from the server, right up to initiating the final render.

## Possible Approaches

The aim is to produce a gradual variation of pose along a curve depending on outside data. producing smooth interpolation between keyframes is difficult to do accurately, and Blender already has this built in. With this in mind, the two approaches I've come across so far are:
1. Take keyframes for every *pose*, and attempt to produce interpolation within the json\_to\_fcurve.py script. This would inevitably mean that interpolation would be linear for simplicity's sake and to avoid introduction of error. However, it means that less data must be exported from Blender.
2. Bake the F-Curves in a pre-made sequence cycling through all adjacent poses, and export every keyframe. E.g generate a keyframe for every 0.5 degrees celcius, and choose one for the current temperature. Then export keyframes instead of f-curves and the interpolation between poses will roughly match that of the original animation

## Files
### Input
CSV Files for each pose in the figure's repertoire (relaxed, comfortable, cold, colder, freezing... dead, etc.)
JSON object pulled from server containing all the launch data in sub-objects.

### Output
####For the pose of the figure:
72 Bones worth of CSV files with frame number and value columns (one for each bone in the skeleton)

10 F-Curves per bone:
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

=> 720 CSV files for pose, unless there turns out to be a nicer way to import into Blender

####For the colour of the skin:
3 CSV files with frame number and colour value for R, G and B channels of diffuse skin colour

