import queue
import numpy as np


class TestQueue:
    def __init__(self, servers, serverMu):
        # TODO: Use queue for advanced cases
        # self.Queue = queue.Queue()

        self.Queue = []
        self.Servers = servers
        self.ServerMu = serverMu

        # TODO: Implement length and queue time

    def Put(self, id):
        self.Queue.append(id)

    def Pop(self):
        return self.Queue.pop(0)

    def PopForTimeStep(self, dt):
        # TODO: Calc timestep in relation to serverMu
        nItems = len(self.Queue)
        # TODO: Randomize
        nItemsToPop = int(np.round(self.Servers*self.ServerMu*dt))
        popped = []

        for _ in range(min(nItems, nItemsToPop)):
            popped.append(self.Pop())

        return popped
