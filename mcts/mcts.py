import random, math, json

from datetime import datetime
from typing import Dict

from numpy import double
from mcts import treeNode

from mcts.treeNode import TreeNode
from sim.simInterface import SimInterface

# TODO: Pull sim out of mcts.

# This funciton should simply handle tree creatin, tuneing and traversal.

# Loop should be splitt into
    #  selectLeafNode: Traverse the tree form the root, checking each traversed node for expansion. Returns seed action sequence to leaf.
    #  rollout: Inputs 
    #  backpropagate:

# Functions are to be called from handler, and the simulator should also be forwarded from there.
# Handler should call selectionToLeafNode, Rollout, Backprop. Future possibilities are reroot and reset.

class MCTS:  
    
    def __init__(self) -> None:
        self.rootNode = TreeNode(None, None)  # NOTE: Might cause problems with None action, but it is correct. T=0
        self.rootNode.visitNode()
        self.currentNode = self.rootNode
        self.simIntefrace = SimInterface()
        self.endStates = []
        self.crashStates = []
        self.leafNode = False
        self.bestState = None
        self.bestReward = -math.inf
        with open("parameters.json") as f:
            params = json.load(f)   # Pass out to controller
        self.k = params["expansion_coefficient"]
        self.a = params["expansion_exponentioal"]
        self.MCT : Dict[tuple, TreeNode] = {}

# ~~~ Selection and progressive widening ~~ #

    def selectNextNode(self) -> int:  # Returns next action towards a leaf node. Should happen in paralell with simulator.
        if len(self.currentNode.children) <= self.k*self.currentNode.timesVisited**self.a:  # Prog wideniung
            self.addRandomChild()
        selectedNode = self.currentNode.uctSelect()
        # if selectedNode is None:  # If no children foundleaf node, initiate node.
        #     selectedNode = self.addRandomChild(self.currentNode)
        if selectedNode.timesVisited == 0:  # If first time visiting, it should be a leaf node.
            self.leafNode = True
        self.currentNode = selectedNode
        return selectedNode.action
    
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
        if self.currentNode.stepReward != None:
            if self.currentNode.stepReward != p:
                print("Noise has been introduced:", self.currentNode.stepReward, p)
        self.currentNode.stepReward = p

    def rollout(self) -> double:
        return random.random()

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
        maxEval = -math.inf
        successor = None
        for child in self.rootNode.children.values():
            if maxEval < child.evaluation:
                maxEval = child.evaluation
                successor = child
        self.currentNode = successor
        self.rootNode = successor
        return successor.action