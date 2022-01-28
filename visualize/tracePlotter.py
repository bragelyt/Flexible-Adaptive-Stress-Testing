from timeit import repeat
from sim.simInterface import SimInterface
import matplotlib.pyplot as plt
from matplotlib import animation

class TracePlotter:

    def __init__(self) -> None:
        self.sim = SimInterface()
        self.startDelay = 8
        self.frameDelay = 100
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(-10, 110), ylim=(-10, 110))
        self.figObjs = []
    
    def animate(self, actionSeedTrace):
        self.posTraces = self.sim.getPositionTrace(actionSeedTrace)
        for j, boat in enumerate(self.posTraces):
            line, = self.ax.plot([], [], lw=2, zorder=10-j)
            scatterBorder = self.ax.scatter(None, None, s =250, zorder=20-j)
            scatterInner = self.ax.scatter(None, None, s =150, c = "white", zorder=30-j)
            self.figObjs.append({"line": line, "scatterBorder": scatterBorder, "scatterInner": scatterInner})
        anim = animation.FuncAnimation(self.fig, self.animateFrame, 
                                    frames=len(self.posTraces[0])-1+self.startDelay, interval=self.frameDelay, repeat = False)
        plt.show()

    def animateFrame(self, i):
        i = i-self.startDelay
        if i < 0:
            i = 0
        for j, boatTrace  in enumerate(self.posTraces):
            x = []
            y = []
            for pos in boatTrace[:i+1]:
                x.append(pos[0])
                y.append(pos[1])
            self.figObjs[j]["line"].set_data(x,y)
            self.figObjs[j]["scatterBorder"].set_offsets([x[-1], y[-1]])
            self.figObjs[j]["scatterInner"].set_offsets([x[-1], y[-1]])