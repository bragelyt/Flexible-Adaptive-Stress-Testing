import json, math

for filename in ["multipleSingleTrees"]:

    # with open("results/nnResults/fullRun500Nodes/"+filename+ ".json", 'r') as f:
    #     stats = json.load(f)

    with open(filename+".json", "r") as f:
        stats = json.load(f)
        
    nrOfFailures = 0
    cumFailure = 0
    cumReward = 0
    bestReward = -math.inf
    for key in stats:
        reward = stats[key]["maxReward"]
        if reward > 0:
            nrOfFailures += 1
            cumFailure += reward
        if reward > bestReward:
            bestReward = reward
        cumReward += reward
    nrOfIts = len(stats)

    print("Nr of failures:", nrOfFailures, "of", nrOfIts)
    print("Best reward:", bestReward)
    print("Avg reward:", cumReward/nrOfIts)
    print("Avg failure reward:", cumFailure/nrOfFailures)