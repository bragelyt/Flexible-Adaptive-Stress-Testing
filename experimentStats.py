
# import random

# distPrediction  = [0.1,0,0,0,0,0,0,0,.45,.45]

# for i in range(10):
#     roulette = random.random()
#     summedActions = 0
#     for index, action in enumerate(distPrediction):
#         summedActions += action
#         if summedActions >= roulette:
#             print(random.random()/len(distPrediction) + index/len(distPrediction))  # TODO: Make pretty
#             break

import json, time

from datetime import datetime



# with open("fileName.json", 'w') as f:
#     json.dump(dataDict, f, indent=4)

fileNames = ["loadfullNNStats", "fullNNstats", "rolloutPolicyStats", "valuePolicyStats", "noNetworkStats"]

for fileName in fileNames:

    with open(fileName+".json", 'r') as f:
        normal200 = json.load(f)

    depthDict = {}
    bestIndex = []
    globalBest = -150
    bestPrDepth = []
    bestCrashPrDepth = []
    bestDepths = {}
    bestCrashDepths = {}
    avgs = []
    for i, itt in normal200.items():
        localBest = -150
        bestDepth = None
        for depth in itt:
            depthBest = itt[depth]["maxReward"]
            depthAvg = itt[depth]["avg"]
            avgs.append(depthAvg)
            if localBest < depthBest:
                bestDepth = int(depth)
                localBest = depthBest
                localBestTrace = itt[depth]["route"]
        bestPrDepth.append(localBest)
        if bestDepth not in bestDepths.keys():
            bestDepths[bestDepth] = 0
        bestDepths[bestDepth] += 1
        if localBest > 0:
            bestIndex.append(int(i))
            bestCrashPrDepth.append(localBest)
            if bestDepth not in bestCrashDepths:
                bestCrashDepths[bestDepth] = 0
            bestCrashDepths[bestDepth] += 1
        if localBest > globalBest:
            globalBest = localBest
            bestTrace = localBestTrace


    for i, itt in normal200.items():
        for depth in itt:
            depthBest = itt[depth]["maxReward"]
            if depthBest > 0:
                if int(depth) not in depthDict.keys():
                    depthDict[int(depth)] = 0
                depthDict[int(depth)] += 1
                break

    firstFailureDepth = ""
    for i in range(18):
        if i in depthDict.keys():
            firstFailureDepth += f"{i}: {depthDict[i]}, "

    # sum = 0
    depthBestCrash = ""
    for i in range(18):
        if i in bestCrashDepths.keys():
            depthBestCrash += f"{i}: {bestCrashDepths[i]}, "
            # sum += bestCrashDepths[i]
    # print("crashes", sum)
    
    # sum = 0
    depthBest = ""
    for i in range(18):
        if i in bestDepths.keys():
            depthBest += f"{i}: {bestDepths[i]}, "
            # sum += bestDepths[i]
    # print("200", sum)

    nrOfCrashes=0
    avgDepth = 0
    for i, value in depthDict.items():
        nrOfCrashes += value
        avgDepth += value * i
    avgDepth = avgDepth/nrOfCrashes

    nrOfBestCrashes=0
    avgBestCrashDepth = 0
    for i, value in depthDict.items():
        nrOfBestCrashes += value
        avgBestCrashDepth += value * i
    avgBestCrashDepth = avgBestCrashDepth/nrOfBestCrashes
    
    nrOfLoops=0
    avgBestDepth = 0
    for i, value in bestDepths.items():
        nrOfLoops += value
        avgBestDepth += value * i
    avgBestDepth = avgBestDepth/nrOfLoops

    # AVG best reward
    # Avg crash reward
    

    print("---------")
    print(fileName, nrOfCrashes, nrOfBestCrashes, nrOfLoops)
    print("---------")
    print("failures found", nrOfCrashes)
    print("total avg reward:", sum(avgs)/len(avgs))
    print("global best reward", globalBest)
    print("avg best reward of trees", sum(bestPrDepth)/len(bestPrDepth))
    print("avg best reward when E of trees", sum(bestCrashPrDepth)/len(bestCrashPrDepth))
    print("---------")
    print("avg depth of first crash", avgDepth/nrOfCrashes)
    print("avg depth of best:", avgBestDepth)
    print("avg depth of best when E:", avgBestCrashDepth)
    print("depth of first failures:", firstFailureDepth)
    print("dephts of bests:", depthBest)
    print("depths of best failures:", depthBestCrash)
    print("---------")
    print("best trace", bestTrace)
    print("---------")
    print("best indexes", len(bestIndex), bestIndex)

# print(normal200["1"]["18"])