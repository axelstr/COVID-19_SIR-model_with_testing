import numpy as np

from .server import Server


class TestQueue:
    """Testing queue object.
    """

    def __init__(self, nServers, serverMu, prioritisation):
        self.Prioritisation = prioritisation

        self.Queue = []
        # TODO: Test with 2.75
        self.NServers = nServers
        self.Servers = [Server(serverMu, 1) for n in range(int(nServers))]
        if nServers % 1 != 0:
            self.Servers.append(Server(serverMu, nServers % 1))
        self.ServerMu = serverMu

    def put(self, id):
        """Appends an element last in the queue.
        """
        self.Queue.append(id)

    def pop(self):
        """Pops an element depending on the prioritization policy.
        FIFO: First.
        LIFO: Last.
        """
        if self.Prioritisation == 'FIFO':
            return self.Queue.pop(0)
        elif self.Prioritisation == 'LIFO':
            return self.Queue.pop()
        else:
            raise Exception(
                f"Prioritization [{self.Prioritisation}] is not valid.")

    def simulateDay(self):
        """Simulates a day where each server handles a number of depending on serverMu.
        """
        nItems = len(self.Queue)
        nItemsToPop = 0
        popped = []

        for server in self.Servers:
            nItemsToPop += server.simulateDay()

        for _ in range(min(nItems, nItemsToPop)):
            popped.append(self.pop())

        return popped

    def renegade(self, idsToRenegade):
        """Removes the given ids from the queue.
        """
        self.Queue = [id for id in self.Queue if (not id in idsToRenegade)]

    def getExpectedQueueTime(self):
        """The current, expected waiting time for the last person in the queue.
        """
        if self.Servers == 0:
            return np.NaN

        queued = max(len(self.Queue)-len(self.Servers), 0)
        expectedQueueTime = queued*self.ServerMu/self.NServers

        return expectedQueueTime

    def getQueueLength(self):
        """The current number of people queued.
        """
        return len(self.Queue)
