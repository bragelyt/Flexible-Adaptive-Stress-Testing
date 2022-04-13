from __future__ import annotations
from sim.zeabuzInterface import ZeabuzSimInterface

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Noise")
    zSim.plotSavedPath("Crash4000", rate = 20, borders = True, noise=False)

if __name__ == "__main__":
    zeabuzPlotter()