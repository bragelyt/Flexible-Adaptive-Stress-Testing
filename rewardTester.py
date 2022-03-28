import math, json

actionSequence = [0.97, 0.98, 0.96, 0.88, 0.97, 0.99, 0.67, 0.86, 0.71, 0.65, 0.55, 0.4, 0.64, 0.48, 0.54, 0.59]

transProb = 0
with open('rewards.json') as f:
    rewards = json.load(f)

rs = []
for values in rewards:
    actionSequence = values[2]    
    transProb = 0
    for i in range(1, len(actionSequence)):
        transProb += math.log(1-abs(actionSequence[i] - actionSequence[i-1]))
    if values[1][0]:
        reward = transProb + 10
    else:
        reward = transProb - values[1][1]
    if round(reward,2) != round(values[0],2):
        print(reward, values[0])
    rs.append(reward)
print("max", max(rs))