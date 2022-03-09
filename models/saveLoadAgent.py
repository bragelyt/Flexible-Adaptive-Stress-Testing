import torch
import json
from models.neuralNetwork import NeuralActor
from shutil import copyfile

def LoadModel(fileName):
    with open('project2/parameters.json') as f:
        parameters = json.load(f)
    modelSaveLocation = parameters["model_save_location"]
    optimizer = parameters["anet_optimizer"]
    learningRate = parameters["anet_learning_rate"]
    lossFunction = parameters["loss_function"]

    model = torch.load(modelSaveLocation+fileName)

    print("loaded model", fileName)
    return NeuralActor(
        model=model,
        optimizer=optimizer,
        learningRate=learningRate,
        lossFunction=lossFunction,
    )

def SaveModel(model, fileName):
    with open('project2/parameters.json') as f:
        parameters = json.load(f)
    modelSaveLocation = parameters["model_save_location"]
    path = modelSaveLocation+fileName
    torch.save(model, path)
    copyParameterFile(path + "_parameters.json")
    print("Saved model", fileName)

def copyParameterFile(path: str) -> None:
    copyfile("./project2/parameters.json", path)
