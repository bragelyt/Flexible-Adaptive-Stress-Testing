import torch, json, random
import torch.nn as nn
import torch.nn.functional as F
from typing import List
import torch.optim as optim

class NeuralNetwork(nn.Module):

    def __init__(self, activationFunction, networkType):
        self.activationFunction = activationFunction
        super(NeuralNetwork, self).__init__()
        self.layers = nn.ModuleList()
        if "input" in networkType.keys():
            self.layers.append(nn.Linear(in_features=networkType["input"]["in_features"], out_features=networkType["input"]["out_features"]))
        for layer, args in networkType.items():
            if layer.startswith("linear"):
                self.layers.append(nn.Linear(in_features=args["in_features"], out_features=args["out_features"]))
            elif layer.startswith("conv"):
                self.layers.append(nn.Conv2d(
                    in_channels = args["in_channels"],  # Number of 2d layers
                    out_channels = args["out_channels"], 
                    kernel_size = args["kernel_size"], # Size of filter(width)
                    padding = args["padding"]) # Ramme med 0 rundt gameboard
                )
            elif layer.startswith("flatten"):
                self.layers.append(nn.Flatten())
        if "output" in networkType.keys():
            self.layers.append(nn.Linear(in_features=networkType["output"]["in_features"], out_features=networkType["output"]["out_features"]))
        print(self.layers)

    def forward(self, input):
        for index, layer in enumerate(self.layers):
            if index == 0:
                input = layer(input)
            elif index == len(self.layers) - 1:
                input = F.softmax(layer(input), dim=0)
            else:
                if(self.activationFunction == "relu"):
                    input = F.relu(layer(input))
                elif(self.activationFunction == "linear"):
                    input = layer(input)
                if(self.activationFunction == "sigmoid"):
                    input = torch.sigmoid(layer(input))
                if(self.activationFunction == "tanh"):
                    input = torch.tanh(layer(input))
        return input

class NetworkPolicy:
    def __init__(self,
            networkType,
            model = None,
            optimizer=None,
            learningRate=None,
            lossFunction=None):
        self.networkType = networkType
        if networkType.endswith("Rollout"):
            parms = "RolloutSetup"
        elif networkType.endswith("Value"):
            parms = "ValueSetup"
        with open('models/networkParameters.json') as f:
            parameters = json.load(f)
        optimizer = optimizer if optimizer is not None else parameters[parms]["optimizer"]
        lossFunction = lossFunction if lossFunction is not None else parameters[parms]["loss_function"]
        learningRate = learningRate if learningRate is not None else parameters[parms]["learning_rate"]
        activation = parameters[parms]["activation_function"]
        if model == None:
            self.neuralNet = NeuralNetwork(
                activationFunction = activation,
                networkType = parameters[networkType])
        else:
            self.neuralNet = model
        if optimizer != None:
            if optimizer.lower() == "sgd":
                self.optimizer = optim.SGD(self.neuralNet.parameters(), lr = learningRate)
            elif optimizer.lower() == "adam":
                self.optimizer = optim.Adam(self.neuralNet.parameters(), lr = learningRate)
            elif optimizer.lower() == "rmsprop":
                self.optimizer = optim.RMSprop(self.neuralNet.parameters(), lr = learningRate)
            elif optimizer.lower() == "adagrad":
                self.optimizer = optim.Adagrad(self.neuralNet.parameters(), lr = learningRate)
        if lossFunction != None:
            if lossFunction.lower() == "mse":        
                self.lossFunc = nn.MSELoss()
            elif lossFunction.lower() == "mae":
                self.lossFunc = nn.L1Loss()
            elif lossFunction.lower() == "cc":
                self.lossFunc = CCLoss()
        else: self.lossFunc = nn.MSELoss()

    def trainOnBatch(self, batch):
        for item in batch:  # Item = [state -> [-1, board as list], actionDist -> [actios]
            self.train(item[0], item[1])
    
    def train(self, state, target):
        # print(state[0], [round(x, 2) for x in target])
        state = [float(x) for x in state] 
        # state = [float(state[0])/100]
        target = [float(x) for x in target] 
        input = torch.tensor(
            state, dtype=torch.float32)
        self.optimizer.zero_grad()
        output = self.neuralNet(input)
        output = self.lossFunc(output, torch.tensor(target))
        output.backward(retain_graph = True)
        self.optimizer.step()
    
    def getRolloutAction(self, state):
        actionDist = self.getPrediction(state)
        return actionDist

    def getPrediction(self, state: List):
        # state = [state[0]/100]
        input = torch.tensor(
            state, dtype=torch.float32)
        self.optimizer.zero_grad()
        output = self.neuralNet(input)
        return output.detach().numpy()

class CCLoss(nn.Module):
    def init(self):
        super(CCLoss,self).init()

    def forward(self, x, y):
        return -(y * torch.log(x)).sum(dim=1).mean()