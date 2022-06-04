# %%
import matplotlib.pyplot as plt

c = {
    "Both NN": "C2", # "forestgreen"
    "Rollout policy": "C0", #"indigo"
    "Value network":"C1", #orange
    "No NN": "C3", # "gray"
    "MCTS-SA/No NN": "k", # "red"
    "MCTS-SA": "k",
}

rootPruneIncrease = 1.81

runtimeAdditions = {
    "Both NN": 0.008141,
    "Rollout policy": 0.002179,
    "Value network":0.003457,
    "MCTS-SA/No NN": 0
}

runtimes = []

for i in range(50000):
    runtimes.append((i+1)/50000)

# # %%

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
#     print(setup, relativeRuntime[setup][-1])
#     plt.plot(runtimes, relativeRuntime[setup], c = c[setup])

# plt.legend(list(runtimeAdditions.keys()), loc ='lower right')

# plt.title("Neural network impact on nr. simulations run")
# plt.xscale('log', base=10) 
# plt.xlabel('Simulation runtime (sec)')
# plt.ylabel('Relative nr. of simulations over time')
# # plt.yscale('log',base=10) 

# plt.show()

# # %%


# failureRate = {
#     "Both NN": 39,
#     "Rollout policy": 37,
#     "Value network": 20.5,
#     "No NN": 29.5,
#     "MCTS-SA": 35.5
# }

# runtimeAdditions = {
#     "Both NN": 0.008141,
#     "Rollout policy": 0.002179,
#     "Value network":0.003457,
#     "No NN": 0,
#     "MCTS-SA": 0
# }


# relativeFailure = {}
# failuresOverTime = {}

# for setup in failureRate:
#     relativeFailure[setup] = []
#     for runtime in runtimes:
#         if setup == "MCTS-SA":
#             relativeFailure[setup].append(1)
#         else:
#             addition = runtimeAdditions[setup]
#             relatifeFailureRate = failureRate[setup]/failureRate["MCTS-SA"]
#             RelativeR =  rootPruneIncrease*runtime/(addition + runtime)*relatifeFailureRate
#             relativeFailure[setup].append(RelativeR)
#     print(setup, relativeFailure[setup][-1])
#     plt.plot(runtimes, relativeFailure[setup], c = c[setup])

# plt.legend(list(runtimeAdditions.keys()), loc ='lower right')

# plt.title("Neural network impact on failure finding rate")
# plt.xscale('log', base=10) 
# plt.xlabel('Simulation run time (sec)')
# plt.ylabel('Relative nr. of failures found over time')
# # plt.yscale('log',base=10) 

# plt.show()

# rootPruneIncrease = 1.81

runtimeAdditions = {
    "No NN": 0,
    "MCTS-SA": 0,
    "Both NN": 0.008141,
    "Rollout policy": 0.002179,
    "Value network":0.003457,
}

runtimes = []

for i in range(50000):
    runtimes.append((i+1)/50000)

# %%

relativeRuntime = {}
absRuntimes = []

for setup in runtimeAdditions:
    relativeRuntime[setup] = []
    for i, runtime in enumerate(runtimes):
        if setup == "MCTS-SA":
            relativeRuntime[setup].append(1)
        elif setup == "No NN":
            absRuntime = 0.000200555556 + 0.55*runtime
            absRuntimes.append(absRuntime)
            relativeRuntime[setup].append(runtime/absRuntime)
        else:
            addition = runtimeAdditions[setup]
            RelativeR =  runtime/(addition + absRuntimes[i])
            relativeRuntime[setup].append(RelativeR)
    print(setup, relativeRuntime[setup][-1])


legends = []
for setup in list(c.keys()):
    if setup in relativeRuntime.keys():
        plt.plot(runtimes, relativeRuntime[setup], c = c[setup])
        legends.append(setup)

plt.legend(legends, loc ='lower right')

plt.title("Neural network impact on nr. simulations run w/ periodic root pruning")
plt.xscale('log', base=10) 
plt.xlabel('Simulation runtime (sec)')
plt.ylabel('Relative nr. of simulations over time')
# plt.yscale('log',base=10) 

plt.show()

# %%

overOne = {}
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
    overOne[setup] = None
    for i, runtime in enumerate(runtimes):
        if setup == "MCTS-SA":
            RelativeR = 1
        elif setup == "No NN":
            absRuntime = 0.000200555556 + 0.55*runtime
            relatifeFailureRate = failureRate[setup]/failureRate["MCTS-SA"]
            RelativeR = relativeRuntime[setup][i]*relatifeFailureRate
        else:
            addition = runtimeAdditions[setup]
            relatifeFailureRate = failureRate[setup]/failureRate["MCTS-SA"]
            RelativeR =  relativeRuntime[setup][i]*relatifeFailureRate
        relativeFailure[setup].append(RelativeR)
        if RelativeR > 1 and overOne[setup] is None:
                overOne[setup] = runtime
    print("max", setup, relativeFailure[setup][-1])
    print("pass", setup, overOne[setup])

legends = []
for setup in list(c.keys()):
    if setup in relativeFailure.keys():
        plt.plot(runtimes, relativeFailure[setup], c = c[setup])
        legends.append(setup)

plt.legend(legends, loc ='lower right')
plt.title("Neural network impact on failure finding rate \w root pruning")
plt.xscale('log', base=10) 
plt.xlabel('Simulation run time (sec)')
plt.ylabel('Relative nr. of failures found over time')
# plt.yscale('log',base=10) 

x = [0.00072, 0.015, 0.196214]
y = [1.00, 1.48, 1.85]


plt.plot(x, y, marker='o', c = "black", linestyle = 'None')
for i, j in zip(x, y):
   plt.text(i*0.08, j+0.07, f'({round(i*1000,2)}ms, {j})')

plt.show()