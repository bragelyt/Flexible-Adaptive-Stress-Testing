import json

with open("multipleSingleTrees.json", 'r') as f:
    stats = json.load(f)


nrOfFailures = 0
cumFailure = 0
cumReward = 0
for key in stats:
    reward = stats[key]["maxReward"]
    if reward > 0:
        nrOfFailures += 1
        cumFailure += reward
    cumReward += reward
nrOfIts = len(stats)

print("Nr of failures:", nrOfFailures, "of", nrOfIts)
print("Avg reward:", cumReward/nrOfIts)
print("Avg failure reward:", cumFailure/nrOfFailures)