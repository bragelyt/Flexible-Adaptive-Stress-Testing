from __future__ import annotations
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface
from datetime import datetime

def simpleNoTrain():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=True, 
        rolloutPolicy = "SimpleRollout", 
        valuePolicy = "SimpleValue",
        loadModel = False, 
        saveModel = False, 
        train = False)
    mctsHandler.buildDescendingTree(nrOfTrees= 200, treeDepth= 18, loopsPrRoot= 500)
    return(datetime.now()-start)

def simpleTrain():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=True, 
        rolloutPolicy = "SimpleRollout", 
        valuePolicy = "SimpleValue",
        loadModel = False, 
        saveModel = True, 
        train = True)
    mctsHandler.buildDescendingTree(nrOfTrees= 200, treeDepth= 18, loopsPrRoot= 500)
    return(datetime.now()-start)

def simpleLoad():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=True, 
        rolloutPolicy = "SimpleRollout", 
        valuePolicy = "SimpleValue",
        loadModel = True, 
        saveModel = False, 
        train = False)
    mctsHandler.buildDescendingTree(nrOfTrees= 200, treeDepth= 18, loopsPrRoot= 500)
    return(datetime.now()-start)

def zeabuz():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Delay", route=True, steerablePaths = "turn_left")
    mctsHandler = MCTSHandler(
        zSim, 
        plotBest=False, 
        rolloutPolicy = "ZeabuzRollout", 
        valuePolicy = "ZeabuzValue",
        loadModel = True, 
        saveModel = True, 
        train = True)
    mctsHandler.buildDescendingTree(10, 18, 5)

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Noise")
    zSim.plotSavedPath("300322Delay36h", rate = 20, borders = True, noise=False)

if __name__ == "__main__":
    noTrainTime = simpleNoTrain()
    trainTime = simpleTrain()
    print("noTrainTime", noTrainTime)
    print("trainTime", trainTime)