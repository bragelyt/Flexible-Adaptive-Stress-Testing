from __future__ import annotations
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface
from visualize.tracePlotter import TracePlotter
from datetime import datetime


def setup1():
    start = datetime.now()
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Delay", route=True, steerablePaths = "turn_left")
    mctsHandler = MCTSHandler(
        zSim, 
        verbose=False,
        plotBest=False,
        rolloutPolicy = "ZeabuzRollout", 
        valuePolicy = "ZeabuzValue",
        loadModel = False, 
        saveModel = False, 
        train = True)
    mctsHandler.buildDescendingTree(15, 22, 50, setInternalState=False)
    return(datetime.now()-start)
    
def setup2():
    start = datetime.now()
    zSim = ZeabuzSimInterface("delay_scenario2", mode="Delay", route=True, steerablePaths = "straight")
    mctsHandler = MCTSHandler(
        zSim, 
        verbose=False,
        plotBest=False,
        rolloutPolicy = "ZeabuzRollout", 
        valuePolicy = "ZeabuzValue",
        loadModel = False, 
        saveModel = False, 
        train = True)
    mctsHandler.buildDescendingTree(15, 22, 50, setInternalState=False)
    return(datetime.now()-start)

def setup3():
    start = datetime.now()
    zSim = ZeabuzSimInterface("delay_scenario3", mode="Delay", route=True, steerablePaths = "straight")
    mctsHandler = MCTSHandler(
        zSim, 
        verbose=False,
        plotBest=False,
        rolloutPolicy = "ZeabuzRollout", 
        valuePolicy = "ZeabuzValue",
        loadModel = False, 
        saveModel = False, 
        train = True)
    mctsHandler.buildDescendingTree(15, 22, 50, setInternalState=False)
    return(datetime.now()-start)

def setup4():
    start = datetime.now()
    zSim = ZeabuzSimInterface("delay_scenario4", mode="Delay", route=True, steerablePaths = "turn_left_gradual")
    mctsHandler = MCTSHandler(
        zSim, 
        verbose=False,
        plotBest=False,
        rolloutPolicy = "ZeabuzRollout", 
        valuePolicy = "ZeabuzValue",
        loadModel = False, 
        saveModel = False, 
        train = True)
    mctsHandler.buildDescendingTree(15, 22, 50, setInternalState=False)
    return(datetime.now()-start)

print("setup4", setup4())