from sim.simInterface import SimInterface
from datetime import datetime
import random

SI = SimInterface()

start = datetime.now()
for i in range(100000):
    SI.resetSim()
    while not SI.isTerminal():
        SI.step(0.6)

print(i, datetime.now()-start)