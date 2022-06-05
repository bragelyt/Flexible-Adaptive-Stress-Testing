import math, json

actionSequence =[0.9871356646603979, 0.9547478814892288, 0.9987622820928191, 0.9556341629616887, 0.972181669893422, 0.8989967291946668, 0.9684663237258985, 0.7767886241916577, 0.7513153050894681, 0.5078161202685887, 0.3623055277372267, 0.6108366901760816, 0.611096425941908, 0.33554570767599434, 0.45387563842044576, 0.5627031095323771, 0.44296479689961765]

# transProb = 0
# with open('rewards.json') as f:
#     rewards = json.load(f)

# rs = []
# for values in rewards:
# actionSequence = values[2]    
transProb = 0
for i in range(1, len(actionSequence)):
    transProb += math.log(1-abs(actionSequence[i] - actionSequence[i-1]))
# if values[1][0]:
#     reward = transProb + 10
# else:
#     reward = transProb - values[1][1]
# if round(reward,2) != round(values[0],2):
#     print(reward, values[0])
# rs.append(reward)
# print("max", max(rs))

print(30+transProb)