import queue
import numpy as np

from exp_randomizer import ExpRandomizer


class TestQueue:
    def __init__(self, servers, serverMu, prioritisation='FIFO'):
        # TODO: Use queue for advanced cases
        # self.Queue = queue.Queue()
        self.ExpRandomizer = ExpRandomizer()
        self.Prioritisation = prioritisation

        self.Queue = []
        self.Servers = servers
        self.ServerMu = serverMu

        # TODO: Implement length and queue time getters

    def Put(self, id):
        self.Queue.append(id)

    def Pop(self):
        if self.Prioritisation == 'FIFO':
            return self.Queue.pop(0)
        if self.Prioritisation == 'LIFO':
            return self.Queue.pop()

    def PopForOneDay(self):
        # TODO: Implement queue with ExpRandomizer
        nItems = len(self.Queue)
        nItemsToPop = int(np.round(self.Servers*self.ServerMu))
        popped = []

        for _ in range(min(nItems, nItemsToPop)):
            popped.append(self.Pop())

        return popped
