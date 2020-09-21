import numpy as np

from .exp_randomizer import ExpRandomizer


class TestQueue:
    """Testing queue object.
    """

    def __init__(self, servers, serverMu, prioritisation):
        self.ExpRandomizer = ExpRandomizer()
        self.Prioritisation = prioritisation

        self.Queue = []
        self.Servers = servers
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
        # TODO: Implement queue with ExpRandomizer
        nItems = len(self.Queue)
        nItemsToPop = int(np.round(self.Servers/self.ServerMu))
        popped = []

        for _ in range(min(nItems, nItemsToPop)):
            popped.append(self.pop())

        return popped

    def renegade(self, idsToRenegade):
        """Removes the given ids from the queue.
        """
        self.Queue = [id for id in self.Queue if (not id in idsToRenegade)]

    def getExpectedWaitingTime(self):
        """The current, expected waiting time for the last person in the queue.
        """
        if self.Servers == 0:
            return np.NaN

        queued = max(len(self.Queue)-self.Servers, 0)
        waitingTimeUntilServed = queued*self.ServerMu/self.Servers

        return waitingTimeUntilServed + self.ServerMu

    def getQueueLength(self):
        """The current number of people queued.
        """
        return len(self.Queue)
