import torch
import json
from models.neuralNet import NetworkPolicy
from shutil import copyfile

def LoadModel(fileName) -> NetworkPolicy:
    networkSaveLocation = "./saved_models/"
    path = networkSaveLocation+fileName
    with open(path+"_parameters.json") as f:
        load = json.load(f)
    networkType = list(load.keys())[1]
    parameters = load["Setup"]
    optimizer = parameters["optimizer"]
    learningRate = parameters["learning_rate"]
    lossFunction = parameters["loss_function"]
    print(lossFunction)
    network = torch.load(networkSaveLocation+fileName)
    print("loaded model", fileName)
    return NetworkPolicy(
        networkType=networkType,
        model=network,
        optimizer=optimizer,
        learningRate=learningRate,
        lossFunction=lossFunction
    )

def SaveNetwork(model, fileName) -> None:
    network = model.neuralNet
    networkType = model.networkType
    networkSaveLocation = "./saved_models/"
    path = networkSaveLocation+fileName
    torch.save(network, path)
    copyParameterFile(path + "_parameters.json", networkType)
    print("Saved network", fileName)

def copyParameterFile(path: str, modelType) -> None:
    with open("models/networkParameters.json") as f:
        fullDict = json.load(f)
    modelDict = {}
    if modelType.endswith("Rollout"):
        modelDict["Setup"] = fullDict["RolloutSetup"]
    elif modelType.endswith("Value"):
        modelDict["Setup"] = fullDict["ValueSetup"]
    modelDict[modelType] = fullDict[modelType]
    with open(path, 'w') as f:
        json.dump(modelDict, f, indent=4)

