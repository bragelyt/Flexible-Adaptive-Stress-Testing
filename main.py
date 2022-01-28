from __future__ import annotations
from mcts.mctsHandler import MCTSHandler

def main():
    mctsHandler = MCTSHandler(plotBest=True, verbose=True)
    mctsHandler.buildSingleTree(6000)

if __name__ == "__main__":
    main()