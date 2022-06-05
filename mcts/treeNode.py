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
        self.stepReward = None
        self.children = {}  # SeedAction, node
        self.stateRepresentation = None
        if self.action == None:
            self.stepReward = 0
        else:
            self.evaluation = 0
        # self.childrenVisits : Dict[tuple, int] = {}  # ChildNodeState, nrOfVisits  # TODO: Change childNodeState to treeNode
        # self.childrenEvaluations : Dict[tuple, tuple] = {}
    
    def visitNode(self):
        self.timesVisited += 1
    
    def addChild(self, newBornAction) -> TreeNode:
        if newBornAction not in self.children.keys():  # REVIEW: Sloppy fix for randomness in seed generation. If exact same seed generated before, a child is not added.
            self.children[newBornAction] = TreeNode(newBornAction, self)  # NOTE This is the backbone of the tree structure
        return self.children[newBornAction]
    
    def getChildDistribution(self, nrOfBuckets):  # TODO: A few things could be done. Look into -1 or -2 to all visits, only taking max pr bucket or exponential visits.
        if len(self.children) == 0:
            return None
        buckets = []
        dist = []
        for i in range(nrOfBuckets):
            bucket = (i+1)/nrOfBuckets
            buckets.append(bucket)
            dist.append(0)
        for actionSeed, node in self.children.items():
            i = 0
            while actionSeed >= buckets[i]:
                i+=1
            dist[i] += node.timesVisited/(self.timesVisited-1)
        return dist

    def eveluate(self, reward): # Called dureing backprop
        self.evaluation = self.evaluation + (reward - self.evaluation)/self.timesVisited
