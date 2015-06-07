# genData.py
# Dylan Auty 7/6/15
#
# Hopefully generates a bunch of data to test the keyframe generation with.

import json

sampleNo = 150	# Number of sample frames to generate
dataDict = {}
currTime = 0	# Simulated time - ms since epoch
timeStep = 1000 # New frame every second right now

for i in (0, sampleNo):
	temp = -50 + i
	dataDict['d'][i] = {
			'CallSign' : 'IMPIBM',
			'seqNo' : i,
			'timestamp' : currTime + timeStep,
			'latitude' : 'nope',
			'longitude' : 'nope',
			'altitude' : 'yes',
			'humidity' : 'like 3 humidity, maybe 4',
			'x' : '1',
			'y' : '2',
			'z' : '3',
			'light' : '2',
			'infrared' : '1',
			'pressure' : '1',
			'internaltemp' : 'blurp',
			'externaltemp' : temp,
			'voltage' : '3.3'
			}

# Output stage
print ("Saving to: ./sampleData.json")

output = open('./sampleData.json', 'w')
output.write(json.dumps(dataDict, indent=4))
output.close()


