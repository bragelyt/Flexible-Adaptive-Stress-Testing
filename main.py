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

def zeabuzZoomState():
    start = datetime.now()
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Delay", route=True, steerablePaths = "turn_left")
    mctsHandler = MCTSHandler(
        zSim, 
        verbose=False,
        plotBest=False)
        # rolloutPolicy = "ZeabuzRollout", 
        # valuePolicy = "ZeabuzValue",
        # loadModel = False, 
        # saveModel = False, 
        # train = True)
    mctsHandler.buildDescendingTree(20, 22, 1, setInternalState=False)
    return(datetime.now()-start)
    
def zeabuzInternalState():
    start = datetime.now()
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Delay", route=True, steerablePaths = "turn_left")
    mctsHandler = MCTSHandler(
        zSim, 
        verbose=False,
        plotBest=False,)
        # rolloutPolicy = "ZeabuzRollout", 
        # valuePolicy = "ZeabuzValue",
        # loadModel = False, 
        # saveModel = False, 
        # train = True)
    mctsHandler.buildDescendingTree(20, 22, 1, setInternalState=True)
    return(datetime.now()-start)

def zeabuzPlotter(fileName):
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Noise")
    zSim.plotSavedPath(fileName, rate = 20, borders = True, noise=False)

if __name__ == "__main__":
    # simpleSingle = simpleSingleTree()
    # noNNTime = noNNSimple()
    # rolloutTime = rolloutNNSimple()
    # valueTime = valueNNSimple()
    # fullNNTime = fullNNSimple()
    # print("simpleSingle", simpleSingle)
    # print("noNNTime", noNNTime)
    # print("rolloutTime", rolloutTime)
    # print("valueTime", valueTime)
    # print("fullNNTime", fullNNTime) 

    # ----- Zeabuz ------ #
    internalState = None
    zoomState = None
    # internalState = zeabuzInternalState()
    print("internalState", internalState)
    zoomState = zeabuzZoomState()
    print("internalState", internalState)
    print("zoomState", zoomState)
    

    # ------ Zeabuz plot ---- #
    # ZP = zeabuzPlotter("zeabuzDelay2022-05-29_14-33-45")