import math, json

from typing import List, Tuple
from numpy import double

from datetime import datetime
from mcts.mcts import MCTS
from visualize.tracePlotter import TracePlotter

def rootPrint(rootNr, maxReward, maxTrace , avgReward, state, pred, isBest):
    text = f'rootDepth: {rootNr:2.0f} | max: {maxReward:8.4f} | avg: {avgReward:8.4f} | best: {str([round(x,2) for x in maxTrace]):126s} | pred: {state:.2f} {[round(x, 3) for x in pred]}'
    if isBest:
        text = '\033[93m' + text + '\033[0m'
    print(text)

def resultPrint(result, iteration, trace):
    if result > 0:
        print(f'\033[93m{result} found at iteration {iteration} | {trace}\033[0m')
    else:
        print(f'\033[91m{result} found at iteration {iteration} | {trace}\033[0m')


class MCTSHandler:

    #TODO: Add funcitons for rerooting tree at most promising node. (Start wiht simple UCT and no exploration?)

    def __init__(self, interface, verbose = True, plotBest = False, rolloutPolicy = None, valuePolicy = None, loadModel= False, saveModel = False, train = True) -> None:
        self.loadModel = loadModel
        self.saveModel = saveModel
        self.train = train
        self.timeStart = str(datetime.now().replace(microsecond=0)).replace(" ","_").replace(":","-")
        self.rolloutPolicyType = rolloutPolicy
        self.valuePolivyType = valuePolicy
        self.simInterface = interface
        if self.simInterface.__class__.__name__ == "ZeabuzSimInterface":
            self.interface = "zeabuz"
            self.verboseInterval = 10
        elif self.simInterface.__class__.__name__ == "SimInterface":
            self.interface = "simple"
            self.verboseInterval = 1000
        self.mcts = MCTS(rolloutPolicy, valuePolicy, self.interface if loadModel else None)
        self.plotBest = plotBest
        self.verbose = verbose
        if plotBest:
            self.plotter = TracePlotter()
    
    def buildSingleTree(self, loops) -> List[double]:
        self.maxReward = -math.inf
        self.bestActionSeedTrace = None
        for i in range(loops):
            self.simInterface.resetSim()
            totalReward, actionSeedTrace = self.loop()
            self.saveBest(totalReward, actionSeedTrace, i)
        print(self.maxReward)
        if self.plotBest:
            self.plotResult()
        return(self.bestActionSeedTrace)

    def buildDescendingTree(self, loopsPrRoot) -> List[double]:  # MCTS should keep track of root
        self.maxReward = -math.inf
        self.bestActionSeedTrace = None
        # rewards = []  # REVIEW: Should be looked at, but rewards are probably correct
        for h in range(100):
            print(f'\033[94m--------- Iteration {h} ----------\033[0m')
            root = self.mcts.reset()
            simState = []
            self.simInterface.resetSim()
            root.stateRepresentation = self.simInterface.getStateRepresentation()
            for i in range(18):
                maxReward = -1000
                cumReward = 0
                self.simInterface.setState(simState)
                isBest = False
                for j in range(loopsPrRoot):
                    self.simInterface.setState(simState)
                    totalReward, actionSeedTrace = self.loop()
                    if totalReward > maxReward:
                        maxReward = totalReward
                        bestPath = actionSeedTrace
                    cumReward += totalReward
                    isBest = self.saveBest(totalReward, actionSeedTrace, j + loopsPrRoot*i) or isBest
                if self.rolloutPolicyType is not None:
                    if self.train:
                        self.simInterface.setState(simState)
                        self.mcts.addNodeToTrainingBatch(self.simInterface.getStateRepresentation())
                nextAction = self.mcts.setNextRoot()
                if nextAction is None:
                    break
                else:
                    simState.append(nextAction)
                # print(simState)
                rootPrint(i, maxReward, bestPath, cumReward / loopsPrRoot, self.simInterface.getStateRepresentation()[0], self.mcts.rolloutPolicy.getPrediction(self.simInterface.getStateRepresentation()), isBest)
            if self.rolloutPolicyType is not None:
                print(f'\033[94m--------- Training {h} ----------\033[0m')
                if self.train:
                    self.mcts.trainRolloutPolicyAtRoot()
                    self.mcts.trainValuePolicyOnTree()
            if self.saveModel:
                self.mcts.saveModel(self.interface, self.rolloutPolicyType, self.valuePolivyType, self.timeStart)
        if self.plotBest:
            self.plotResult()
        print([round(x,4) for x in self.bestActionSeedTrace])
        return(self.bestActionSeedTrace)

    def loop(self) -> Tuple[double, double]:
        #  Selection and progressive widening  #
        p = None
        while not self.mcts.isAtLeafNode() and not self.simInterface.isTerminal():
            nextNode = self.mcts.selectNextNode(self.simInterface.getStateRepresentation())
            actionSeed = nextNode.action
            p = self.simInterface.step(actionSeed)
            nextNode.stateRepresentation = self.simInterface.getStateRepresentation()
        self.mcts.setStepReward(p)
        # --------- Rollout -------- #
        rolloutTransProb = 0
        while not self.simInterface.isTerminal():
            if self.rolloutPolicyType is None:
                actionSeed = self.mcts.rollout()
            else:
                actionSeed = self.mcts.getRolloutPolicy(self.simInterface.getStateRepresentation())
            rolloutTransProb += self.simInterface.step(actionSeed)
        # ------ Backpropagate ----- #
        terminalReward = self.simInterface.terminalReward()
        totalReward = self.mcts.backpropagate(terminalReward + rolloutTransProb)
        self.mcts.setAtRoot()
        actionSeedTrace = self.simInterface.getActionSeedTrace()
        return(totalReward, actionSeedTrace)

    def saveBest(self, totalReward, actionSeedTrace, iterationNr):
        if self.maxReward < totalReward:
            self.maxReward = totalReward
            self.bestActionSeedTrace = actionSeedTrace
            if self.interface == "zeabuz":
                self.simInterface.saveLast(totalReward, actionSeedTrace, self.timeStart)
            if self.verbose:
                resultPrint(totalReward, iterationNr, [round(x,2) for x in actionSeedTrace])
            return True
        return False
        # if self.verbose:  # REVIEW: I overkant?
        #     if iterationNr%self.verboseInterval == 0:
        #         print(iterationNr)
    
    def plotResult(self):
        if self.interface == "zeabuz":
            self.simInterface.plotSavedPath()
        elif self.interface == "simple":
            self.plotter.animate(self.bestActionSeedTrace)
            print(self.maxReward)
        return self.bestActionSeedTrace