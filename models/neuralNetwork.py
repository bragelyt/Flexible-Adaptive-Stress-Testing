import torch
import torch.nn as nn
import torch.nn.functional as F

class NeuralNetwork(nn.Module):

    def __init__(self,
            inputSize,
            outputSize,
            activationFunction):
        self.activationFunction = activationFunction
        super(NeuralNetwork, self).__init__()
        self.layers = nn.ModuleList()
        self.layers.append(nn.Linear(in_features=inputSize, out_features=8))
        self.layers.append(nn.Linear(in_features=8, out_features=32))
        self.layers.append(nn.Linear(in_features=32, out_features=outputSize))
        # for convLayer in convLayersDim:
        #     self.layers.append(nn.Conv2d(
        #         in_channels = convLayer["in"],  # Number of 2d layers
        #         out_channels = convLayer["out"], 
        #         kernel_size = convLayer["kernel"], # Size of filter(width)
        #         padding = convLayer["padding"]) # Ramme med 0 rundt gameboard
        #     )
        # self.layers.append(nn.Flatten())  # Go from 2d output to 1d input
        # denseInput = convLayersDim[-1]["out"] * (inputSize - 1)
        # for numberOfNodes in denseLayersDim:
        #     self.layers.append(nn.Linear(in_features = denseInput, out_features= numberOfNodes))
        #     denseInput = numberOfNodes
        # self.layers.append(nn.Linear(in_features = denseInput, out_features= outputSize))
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

class CCLoss(nn.Module):
    def init(self):
        super(CCLoss,self).init()

    def forward(self, x, y):
        return -(y * torch.log(x)).sum(dim=1).mean()