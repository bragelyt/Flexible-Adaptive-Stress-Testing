from typing import List, Tuple

from numpy import double
from mcts.mcts import MCTS
from visualize.tracePlotter import TracePlotter
import math

class MCTSHandler:

    #TODO: Add funcitons for rerooting tree at most promising node. (Start wiht simple UCT and no exploration?)

    def __init__(self, interface, verbose = True, plotBest = False) -> None:
        self.mcts = MCTS()
        self.sim = interface
        if self.sim.__class__.__name__ == "ZeabuzSimInterface":
            self.interface = "zeabuz"
            self.verboseInterval = 10
        elif self.sim.__class__.__name__ == "SimInterface":
            self.interface = "simple"
            self.verboseInterval = 1000
        self.plotBest = plotBest
        self.verbose = verbose
        if plotBest:
            self.plotter = TracePlotter()
    
    def buildSingleTree(self, loops) -> List[double]:
        maxReward = -math.inf
        bestActionSeedTrace = None
        for i in range(loops):
            totalReward, actionSeedTrace = self.loop()
            if maxReward < totalReward:
                maxReward = totalReward
                bestActionSeedTrace = actionSeedTrace
                if self.verbose: 
                    print(totalReward, "found at itteration", i)
                if self.interface == "zeabuz":
                    self.sim.saveLast()
            if self.verbose:
                if i%self.verboseInterval == 0:
                    print(i)
            self.sim.resetSim()
        if self.plotBest:  # Plot method could be extracted
            if self.interface == "zeabuz":
                self.sim.plotSavedPath()
            elif self.interface == "simple":
                self.plotter.animate(bestActionSeedTrace)
        return bestActionSeedTrace

    def loop(self) -> Tuple[double, double]:
        #  Selection and progressive widening  #
        while not self.mcts.isAtLeafNode() and not self.sim.isTerminal():
            actionSeed = self.mcts.selectNextNode()
            p = self.sim.step(actionSeed)
        self.mcts.setStepReward(p)  # REVIEW:Think noice is gone
        # --------- Rollout -------- #
        rolloutTransProb = 0
        while not self.sim.isTerminal():
            actionSeed = self.mcts.rollout()
            rolloutTransProb += self.sim.step(actionSeed)
        # ------ Backpropagate ----- #
        terminalReward = self.sim.terminalReward()
        totalReward = self.mcts.backpropagate(terminalReward + rolloutTransProb)
        self.mcts.setAtRoot()
        actionSeedTrace = self.sim.getActionSeedTrace()
        return (totalReward, actionSeedTrace)