from __future__ import annotations
import random
from tabnanny import verbose
from mcts import mctsHandler
from mcts.mcts import MCTS
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface
from datetime import datetime


def simple():
    bSim = SimInterface()
    mctsHandler = MCTSHandler(bSim, plotBest=True, verbose=True)
    mctsHandler.buildSingleTree(6000)

def zeabuz():
    zSim = ZeabuzSimInterface("test_scenario")
    mctsHandler = MCTSHandler(zSim, plotBest=False)
    mctsHandler.buildSingleTree(1)

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("test_scenario")
    zSim.plotSavedPath("LastSim", rate = 20, borders = False, noise=True)

if __name__ == "__main__":
    # simple()
    zeabuz()
    zeabuzPlotter()


