from __future__ import annotations
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface
from visualize.tracePlotter import TracePlotter
from datetime import datetime


def setup1():
    start = datetime.now()
    zSim = ZeabuzSimInterface("steer_scenario4", mode="Steer", route=False)
    mctsHandler = MCTSHandler(
        zSim, 
        verbose=False,
        plotBest=False,
        seeds = 2)#,
        # rolloutPolicy = "ZeabuzRollout", 
        # valuePolicy = "ZeabuzValue",
        # loadModel = False, 
        # saveModel = False, 
        # train = True)
    mctsHandler.buildDescendingTree(1, 1, 1, setInternalState=False)
    return(datetime.now()-start)

print("setup1", setup1())