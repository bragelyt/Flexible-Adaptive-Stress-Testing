from __future__ import annotations
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface
from datetime import datetime

# Single tree
def simpleSingleTree():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=False)
    mctsHandler.buildMultipleSingleTree(1000, 9000)
    return(datetime.now()-start)

# Periodic pruning
def noNNSimple():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=False)
    mctsHandler.buildDescendingTree(nrOfTrees= 500, treeDepth= 18, loopsPrRoot= 200)
    return(datetime.now()-start)

def rolloutNNSimple():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=False, 
        rolloutPolicy = "SimpleRollout", 
        valuePolicy = None,
        loadModel = False, 
        saveModel = True, 
        train = True)
    mctsHandler.buildDescendingTree(nrOfTrees= 500, treeDepth= 18, loopsPrRoot= 200)
    return(datetime.now()-start)

def valueNNSimple():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=False, 
        rolloutPolicy = None, 
        valuePolicy = "SimpleValue",
        loadModel = False, 
        saveModel = True, 
        train = True)
    mctsHandler.buildDescendingTree(nrOfTrees= 500, treeDepth= 18, loopsPrRoot= 200)
    return(datetime.now()-start)

def fullNNSimple():
    start = datetime.now()
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=False, 
        verbose=False, 
        rolloutPolicy = "SimpleRollout", 
        valuePolicy = "SimpleValue",
        loadModel = False, 
        saveModel = True, 
        train = True)
    mctsHandler.buildDescendingTree(nrOfTrees= 500, treeDepth= 18, loopsPrRoot= 200)
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
    simpleSingle = simpleSingleTree()
    # noNNTime = noNNSimple()
    # rolloutTime = rolloutNNSimple()
    # valueTime = valueNNSimple()
    # fullNNTime = fullNNSimple()
    print("simpleSingle", simpleSingle)
    # print("noNNTime", noNNTime)
    # print("rolloutTime", rolloutTime)
    # print("valueTime", valueTime)
    # print("fullNNTime", fullNNTime)
    