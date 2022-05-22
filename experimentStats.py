
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

fileNames = ["51of200normalStats", "60of200trainStats"]

for fileName in fileNames:

    with open(fileName+".json", 'r') as f:
        normal200 = json.load(f)

    depthDict = {}
    bestIndex = []
    globalBest = -150
    bestPrDepth = []
    bestCrashPrDepth = []
    avgs = []
    for i, itt in normal200.items():
        localBest = -150
        for depth in itt:
            depthBest = itt[depth]["maxReward"]
            depthAvg = itt[depth]["avg"]
            avgs.append(depthAvg)
            if localBest < depthBest:
                localBest = depthBest
                localBestTrace = itt[depth]["route"]
        bestPrDepth.append(localBest)
        if localBest > 0:
            bestIndex.append(int(i))
            bestCrashPrDepth.append(localBest)
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


    outStr = ""
    for i in range(18):
        if i in depthDict.keys():
            outStr += f"{i}: {depthDict[i]}, "


    cumSum=0
    avgDepth = 0
    for i, value in depthDict.items():
        cumSum += value
        avgDepth += value * i


    # AVG best reward
    # Avg crash reward
    
    print("---------")
    print(fileName)
    print("---------")
    print("avg:", sum(avgs)/len(avgs))
    print("globalBest", globalBest)
    print("AvgBestReward", sum(bestPrDepth)/len(bestPrDepth))
    print("AvgBestCrashReward", sum(bestCrashPrDepth)/len(bestCrashPrDepth))
    print("---------")
    print("failureDepths", outStr)
    print("avg depth", avgDepth/cumSum)
    print("failures found", cumSum)
    print("---------")
    print("bestTrace", bestTrace)
    print("---------")
    print("best indexes", len(bestIndex), bestIndex)

# print(normal200["1"]["18"])