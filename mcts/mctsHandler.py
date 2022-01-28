from typing import List, Tuple

from numpy import double
from sim.simInterface import SimInterface
from mcts.mcts import MCTS
from visualize.tracePlotter import TracePlotter
import math

class MCTSHandler:

    #TODO: Add funcitons for rerooting tree at most promising node. (Start wiht simple UCT and no exploration?)

    def __init__(self, verbose = True, plotBest = False) -> None:
        self.mcts = MCTS()
        self.sim = SimInterface()
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
            if self.verbose:
                if i%1000 == 0:
                    print(i)
        if self.plotBest:
            self.plotter.animate(bestActionSeedTrace)
        return bestActionSeedTrace

    def loop(self) -> Tuple[double, double]:
        #  Selection and progressive widening  #
        while not self.mcts.isAtLeafNode() and not self.sim.isTerminal():
            actionSeed = self.mcts.selectNextNode()
            p = self.sim.step(actionSeed)
        self.mcts.setStepReward(p)  # New node gets transitionProbability set at edge.
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
        self.sim.resetSim()
        return (totalReward, actionSeedTrace)