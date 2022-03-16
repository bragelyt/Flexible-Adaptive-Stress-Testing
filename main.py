from __future__ import annotations
from json import load
from math import pi
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface


def simple():
    bSim = SimInterface()
    mctsHandler = MCTSHandler(
        bSim, 
        plotBest=True, 
        verbose=True, 
        rolloutPolicy = "SimpleRollout", 
        valuePolicy = "SimpleValue",
        loadModel = True, 
        saveModel = True, 
        train = True)
    mctsHandler.buildDescendingTree(500)

def zeabuz():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Delay", route=True, steerablePaths = "turn_left")
    mctsHandler = MCTSHandler(zSim, plotBest=False, rolloutPolicy ="Simple")
    mctsHandler.buildDescendingTree(40)

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Noise")
    zSim.plotSavedPath("LastSim", rate = 20, borders = False, noise=True)

if __name__ == "__main__":
    simple()
    # zeabuz()
    # zeabuzPlotter()