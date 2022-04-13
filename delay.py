from __future__ import annotations
from sim.zeabuzInterface import ZeabuzSimInterface

def zeabuzPlotter():
    zSim = ZeabuzSimInterface("over_turn_scenario", mode="Noise")
    # zSim.plotSavedPath("300322Delay36h", rate = 20, borders = True, noise=False)
    zSim.plotSavedPath("2803Delay165", rate = 20, borders = True, noise=False)

if __name__ == "__main__":
    zeabuzPlotter()