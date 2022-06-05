from __future__ import annotations
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface
from visualize.tracePlotter import TracePlotter
from datetime import datetime


def setup():
    start = datetime.now()
    zSim = ZeabuzSimInterface("steer2", mode="Steer", route=False)
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

print("setup4", setup())
