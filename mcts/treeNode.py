from __future__ import annotations
import math, json
from typing import Dict

class TreeNode:

    def __init__(self, action, parent):
        self.action = action
        self.parrent = parent
        self.isTerminal = False
        # ---------- Stats --------- #
        self.timesVisited = 0  # Initiates only after visit so should be one
        self.evaluation = 0
        if self.action == None:
            self.stepReward = 0
        else:
            self.evaluation = 0

        self.children : Dict[int, TreeNode] = {}
        # self.childrenVisits : Dict[tuple, int] = {}  # ChildNodeState, nrOfVisits  # TODO: Change childNodeState to treeNode
        # self.childrenEvaluations : Dict[tuple, tuple] = {}
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.explorationCoefficient = params["exploration_coefficient"]
    
    def visitNode(self):
        self.timesVisited += 1
    
    def addChild(self, newBornAction) -> TreeNode:
        if newBornAction not in self.children.keys():  # REVIEW: Sloppy fix for randomness in seed generation. If exact same seed generated before, a child is not added.
            self.children[newBornAction] = TreeNode(newBornAction, self)  # NOTE This is the backbone of the tree structure
        return self.children[newBornAction]
    
    def uctSelect(self):  # Tree policy. "Bandit based Monte-Carlo Planning", Kocsis and Szepervari (2006)
        # NOTE: This is left without a check for if children are empty. Should resolve itself through prog widening but might fuck up
        maxValue = -math.inf
        bestChild : TreeNode = None
        for child in self.children.values():
            x = child.evaluation + self.explorationCoefficient*(math.sqrt(math.log(self.timesVisited)/(1+child.timesVisited)))
            if x > maxValue:
                bestChild = child
                maxValue = x
        return bestChild

    def eveluate(self, reward): # Called dureing backprop
        self.evaluation = self.evaluation + (reward - self.evaluation)/self.timesVisited
