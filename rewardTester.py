import math

actionSequence = [0.97, 0.98, 0.96, 0.88, 0.97, 0.99, 0.67, 0.86, 0.71, 0.65, 0.55, 0.4, 0.64, 0.48, 0.54, 0.59]

transProb = 0

for i in range(1, len(actionSequence)):
    transProb += math.log(1-abs(actionSequence[i] - actionSequence[i-1]))

print(10 + transProb)