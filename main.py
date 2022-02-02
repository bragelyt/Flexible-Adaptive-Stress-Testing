from __future__ import annotations
import random
from mcts import mctsHandler
from mcts.mcts import MCTS
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface

def simple():
    mctsHandler = MCTSHandler(SimInterface(), plotBest=True, verbose=True)
    mctsHandler.buildSingleTree(6000)

def zeabuz():
    zSim = ZeabuzSimInterface("test_scenario")
    mctsHandler = MCTSHandler(zSim)
    mctsHandler.buildSingleTree(20)
    zSim.plotSavedPath()
    

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("test_scenario")
    zSim.plotSavedPath("Crash2000", rate = 50)

if __name__ == "__main__":
    # simple()
    zeabuz()