import random, math, json

from datetime import datetime
from typing import Dict

from numpy import double
from mcts import treeNode

from mcts.treeNode import TreeNode
from sim.simInterface import SimInterface
from models.neuralNet import NetworkPolicy
from models.saveLoadAgent import SaveNetwork, LoadModel

# TODO: Pull sim out of mcts.

# This funciton should simply handle tree creatin, tuneing and traversal.

# Loop should be splitt into
    #  selectLeafNode: Traverse the tree form the root, checking each traversed node for expansion. Returns seed action sequence to leaf.
    #  rollout: Inputs 
    #  backpropagate:

# Functions are to be called from handler, and the simulator should also be forwarded from there.
# Handler should call selectionToLeafNode, Rollout, Backprop. Future possibilities are reroot and reset.

class MCTS:  
    
    def __init__(self, rolloutType, valuePolicy, interface) -> None:
        self.rolloutType = rolloutType
        self.valuePolicy = valuePolicy
        self.reset()
        self.simIntefrace = SimInterface()
        if rolloutType is not None:
            if interface is not None:
                try:
                    self.rolloutPolicy = LoadModel(interface, rolloutType) # REVIEW: , batchSize=20)  
                except:
                    print(f"Rollout policy {interface + rolloutType} not found or loaded. New model initiated")
                    interface = None
            if interface is None:
                self.rolloutPolicy = NetworkPolicy(rolloutType) # , batchSize=20)
        if valuePolicy is not None:
            if interface is not None:
                try:
                    self.valuePolicy = LoadModel(interface, valuePolicy) # , batchSize=20)
                except:
                    print(f"Value policy {interface + rolloutType} not found or loaded. New model initiated")
                    interface = None
            if interface is None:
                self.valuePolicy = NetworkPolicy(valuePolicy) # , batchSize=20)
        self.bestState = None
        self.rolloutTrainingBatch = []
        self.rolloutEpsilon = 1.0
        self.bestReward = -math.inf
        with open("parameters.json") as f:
            params = json.load(f)   # Pass out to controller
        self.k = params["expansion_coefficient"]
        self.a = params["expansion_exponentioal"]
        self.explorationCoefficient = params["exploration_coefficient"]
        self.MCT : Dict[tuple, TreeNode] = {}

# ~~~ Selection and progressive widening ~~ #

    def selectNextNode(self, stateRepresentation) -> int:  # Returns next action towards a leaf node. Should happen in paralell with simulator.
        if len(self.currentNode.children) <= self.k*self.currentNode.timesVisited**self.a:  # Prog wideniung
            self.addRandomChild()
        selectedNode = self.uctSelect(stateRepresentation)
        # if selectedNode is None:  # If no children foundleaf node, initiate node.
        #     selectedNode = self.addRandomChild(self.currentNode)
        if selectedNode.timesVisited == 0:  # If first time visiting, it should be a leaf node.
            self.leafNode = True
        self.currentNode = selectedNode
        return selectedNode
    
    def reset(self):
        # self.trainingBatch = []  # REVIEW: Fucker dette ting opp?
        self.rootNode = TreeNode(None, None)  # NOTE: Might cause problems with None action, but it is correct. T=0
        self.originalRoot = self.rootNode
        self.rootNode.visitNode()
        self.currentNode = self.rootNode
        self.endStates = []
        self.crashStates = []
        self.leafNode = False
        return self.rootNode

    def addRandomChild(self) -> TreeNode:
        seedAction = random.random()
        newBornAction = seedAction
        return self.currentNode.addChild(newBornAction)

    def isAtLeafNode(self) -> bool:
        return self.leafNode

    def setAtRoot(self) -> None:  # REVIEW: Trolig litt ubrukelig
        self.leafNode = False

    # def setCurrentNodeTerminal(self):  # REVIEW: Might not need this here. Could be handled in handler
    #     self.currentNode.isTerminal = True
    
    def setStepReward(self, p) -> None:
        if p is None:
            pass
            # print("current step reward:", self.currentNode.stepReward)
        else:
            self.currentNode.stepReward = p
        if self.currentNode.stepReward is not None and p is not None:
            if self.currentNode.stepReward != p:
                print("Noise has been introduced:", self.currentNode.stepReward, p)
        

    def rollout(self) -> double:
        return random.random()
    
    def getRolloutPolicy(self, state):  # REVIEW: Test denne
        # if random.random() > self.rolloutEpsilon:
        #     return self.rollout()
        # else:
        distPrediction = self.rolloutPolicy.getRolloutAction(state)
        summedActions = 0
        cumProb = 0
        exponent = 2
        for prob in distPrediction:
            cumProb += prob**exponent
        roulette = random.random()*cumProb
        for index, action in enumerate(distPrediction):
            summedActions += action**exponent
            if summedActions >= roulette:
                return random.random()/len(distPrediction) + index/len(distPrediction)  # TODO: Make pretty
    
    def saveModel(self, interface, rolloutType, valueType, suffix):
        if self.rolloutType is not None:
            SaveNetwork(self.rolloutPolicy, interface, rolloutType, suffix)
        if self.valuePolicy is not None:
            SaveNetwork(self.valuePolicy, interface, valueType, suffix)

    def addNodeToTrainingBatch(self, state):
        target = self.rootNode.getChildDistribution(nrOfBuckets = 10)
        if target is not None:
            self.rolloutTrainingBatch.append([state, target])

    def trainRolloutPolicyAtRoot(self):
        if self.rolloutPolicy is not None:
            self.rolloutPolicy.trainOnBatch(self.rolloutTrainingBatch)
            self.rolloutTrainingBatch = []

    def trainValuePolicyOnTree(self):
        if self.valuePolicy is not None:
            nodes = [self.originalRoot]
            batch = []
            while len(nodes) > 0:
                node = nodes.pop(0)
                for child in node.children.values():
                    nodes.append(child)
                    trainingValues = [node.stateRepresentation + [child.action], [node.evaluation]]
                    batch.append(trainingValues)
            self.valuePolicy.trainOnBatch(batch)


    def backpropagate(self, reward) -> double:
        while self.currentNode.parrent != None:
            reward = reward + self.currentNode.stepReward  # REVIEW: Might be this simple, but I am tired.
            self.currentNode.visitNode()
            self.currentNode.eveluate(reward)
            self.currentNode = self.currentNode.parrent
        self.currentNode.visitNode()  # REVIEW: Doublecheck that some backrpop is not lost.
        self.currentNode = self.rootNode
        return(reward)
    
    def setNextRoot(self) -> double:
        maxVisits = 0 # REVIEW: Går bort fra max eval til vitits.
        successor = None
        for child in self.rootNode.children.values():
            if maxVisits < child.timesVisited:
                maxVisits = child.timesVisited
                successor = child
        if successor is None:
            return None
        else:
            self.currentNode = successor
            self.rootNode = successor
            return successor.action
    
    def uctSelect(self, stateRepresentation):  # Tree policy. "Bandit based Monte-Carlo Planning", Kocsis and Szepervari (2006)
        # NOTE: This is left without a check for if children are empty. Should resolve itself through prog widening but might fuck up
        maxValue = -math.inf
        bestChild : TreeNode = None
        for child in self.currentNode.children.values():
            # print(stateRepresentation)
            # prediction =  stateRepresentation + [child.action]
            if self.valuePolicy is not None:
                prediction = self.valuePolicy.getPrediction(stateRepresentation + [child.action])[0]
                x = 0.6 * child.evaluation + self.explorationCoefficient*(math.sqrt(math.log(self.currentNode.timesVisited)/(1+child.timesVisited))) + 0.4*prediction
            else:
                x = child.evaluation + self.explorationCoefficient*(math.sqrt(math.log(self.currentNode.timesVisited)/(1+child.timesVisited)))
            if x > maxValue:
                bestChild = child
                maxValue = x
        return bestChild