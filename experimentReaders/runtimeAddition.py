# %%
import matplotlib.pyplot as plt

rootPruneIncrease = 1.85

runtimeAdditions = {
    "Both NN": 0.008141,
    "Rollout policy": 0.002179,
    "Value network":0.003457,
    "No NN": 0,
    "MCTS-SA": 0
}

runtimes = []

for i in range(50000):
    runtimes.append((i+1)/50000)

# %%

# relativeRuntime = {}

# for setup in runtimeAdditions:
#     relativeRuntime[setup] = []
#     for runtime in runtimes:
#         if setup == "MCTS-SA":
#             relativeRuntime[setup].append(1)
#         else:
#             addition = runtimeAdditions[setup]
#             RelativeR = rootPruneIncrease*runtime/(addition + runtime)
#             relativeRuntime[setup].append(RelativeR)
#     plt.plot(runtimes, relativeRuntime[setup])

# plt.legend(list(runtimeAdditions.keys()), loc ='lower right')

# plt.xscale('log',base=10) 
# plt.xlabel('Simulation run time (sec)')
# plt.ylabel('Relative nr. of simulations over time')
# # plt.yscale('log',base=10) 

# plt.show()

# %%


failureRate = {
    "Both NN": 39,
    "Rollout policy": 37,
    "Value network": 20.5,
    "No NN": 29.5,
    "MCTS-SA": 35.5
}

relativeFailure = {}
failuresOverTime = {}

for setup in runtimeAdditions:
    relativeFailure[setup] = []
    for runtime in runtimes:
        if setup == "MCTS-SA":
            relativeFailure[setup].append(1)
        else:
            addition = runtimeAdditions[setup]
            relatifeFailureRate = failureRate[setup]/failureRate["MCTS-SA"]
            RelativeR =  rootPruneIncrease*runtime/(addition + runtime)*relatifeFailureRate
            relativeFailure[setup].append(RelativeR)
    plt.plot(runtimes, relativeFailure[setup])

plt.legend(list(runtimeAdditions.keys()), loc ='lower right')

plt.xscale('log', base=10) 
plt.xlabel('Simulation run time (sec)')
plt.ylabel('Relative nr. of failures found over time')
# plt.yscale('log',base=10) 

plt.show()