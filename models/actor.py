import torch
import torch.nn as nn
import torch.nn.functional as F
import random
from typing import List
import torch.optim as optim
import math
from models.neuralNetwork import NeuralNetwork, CCLoss

class NeuralActor:
    def __init__(self,
            input_size = None,
            output_size = None,
            learningRate = None,
            optimizer = None,
            activation = None,
            lossFunciton = None,
            model = None):
        if model == None:
            self.neuralNet = NeuralNetwork(
                inputSize= input_size,
                outputSize= output_size,
                activationFunction = activation)
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
        if lossFunciton != None:
            if lossFunciton.lower() == "mse":        
                self.lossFunc = nn.MSELoss()
            elif lossFunciton.lower() == "mae":
                self.lossFunc = nn.L1Loss()
            elif lossFunciton.lower() == "cc":
                self.lossFunc = CCLoss()
        else: self.lossFunc = nn.MSELoss()

    def trainOnBatch(self, batch):
        for i in range(20):
            for item in batch:  # Item = [state -> [-1, board as list], actionDist -> [actios]
                    self.train(item[0], item[1])
    
    def train(self, state, target):
        input = torch.tensor(
            state, dtype=torch.float32)
        self.optimizer.zero_grad()
        output = self.neuralNet(input)
        output = self.lossFunc(output, torch.tensor(target))
        output.backward(retain_graph = True)
        self.optimizer.step()

    def getPrediction(self, state: List):
        input = torch.tensor(
            state, dtype=torch.float32)
        self.optimizer.zero_grad()
        output = self.neuralNet(input)
        return output.detach().numpy()