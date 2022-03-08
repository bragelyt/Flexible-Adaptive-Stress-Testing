from __future__ import annotations
from mcts.mctsHandler import MCTSHandler
from sim.simInterface import SimInterface
from sim.zeabuzInterface import ZeabuzSimInterface


def simple():
    bSim = SimInterface()
    mctsHandler = MCTSHandler(bSim, plotBest=True, verbose=True)
    mctsHandler.buildDescendingTree(2000)

def zeabuz():
    zSim = ZeabuzSimInterface("test_scenario_close2", mode="Noise")
    mctsHandler = MCTSHandler(zSim, plotBest=False)
    mctsHandler.buildDescendingTree(150)

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("test_scenario_close2", mode="Noise")
    zSim.plotSavedPath("LastSim", rate = 20, borders = False, noise=True)

if __name__ == "__main__":
    # simple()
    zeabuz()
    # zeabuzPlotter()