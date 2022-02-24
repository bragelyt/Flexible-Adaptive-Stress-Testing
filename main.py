from __future__ import annotations
import random
from statistics import mode
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
    zSim = ZeabuzSimInterface("test_scenario_close2", mode="Noise")
    mctsHandler = MCTSHandler(zSim, plotBest=False)
    mctsHandler.buildSingleTree(4000)

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("test_scenario_close2", mode="Noise")
    zSim.plotSavedPath("LastSim", rate = 20, borders = False, noise=True)

if __name__ == "__main__":
    # simple()
    zeabuz()
    zeabuzPlotter()


