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

import json



# with open("fileName.json", 'w') as f:
#     json.dump(dataDict, f, indent=4)

with open("200normalStats.json", 'r') as f:
    normal200 = json.load(f)

crashes = 0
globalMax = -150
for itt in normal200:
    depth = list(normal200[itt].keys())[-1]
    # depth = "5"
    maxReward= normal200[itt][depth]["maxReward"]
    if maxReward > globalMax:
        globalMax = maxReward
    if maxReward > 0:
        crashes += 1
print(crashes, globalMax)

        
# print(normal200["1"]["18"])