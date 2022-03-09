from __future__ import annotations
from math import pi
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface


def simple():
    bSim = SimInterface()
    mctsHandler = MCTSHandler(bSim, plotBest=True, verbose=True)
    mctsHandler.buildDescendingTree(2000)

def zeabuz():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Delay", route=True, steerablePaths = "turn_left")
    mctsHandler = MCTSHandler(zSim, plotBest=False)
    mctsHandler.buildDescendingTree(40)

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Noise")
    zSim.plotSavedPath("LastSim", rate = 20, borders = False, noise=True)

if __name__ == "__main__":
    # simple()
    zeabuz()
    zeabuzPlotter()