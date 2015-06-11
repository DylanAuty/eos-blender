# genData.py
# Dylan Auty 7/6/15
#
# Hopefully generates a bunch of data to test the keyframe generation with.

import json

sampleNo = 150	# Number of sample frames to generate
tempDict = []
dataDict = {}
currTime = 0	# Simulated time - ms since epoch
timeStep = 1000 # New frame every second right now

for i in range(0, sampleNo):
	temp = -50 + i
	currTime += timeStep
	tempDict.append({
			'CallSign' : 'IMPIBM',
			'seqNo' : i,
			'timestamp' : str(currTime),
			'latitude' : 'nope',
			'longitude' : 'nope',
			'altitude' : str(i * 200),
			'humidity' : 'like 3 humidity, maybe 4',
			'x' : '1',
			'y' : '2',
			'z' : '3',
			'light' : '2',
			'infrared' : '1',
			'pressure' : '1',
			'internaltemp' : 'blurp',
			'voltage' : '3',
			'externaltemp' : str(temp)
			})

# Output stage
print ("Saving to: ./testData.json")
dataDict = {'d' : tempDict}

output = open('./testData.json', 'w')
output.write(json.dumps(dataDict, indent=4))
output.close()


