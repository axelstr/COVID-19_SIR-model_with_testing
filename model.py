# SIR Model with M|M|s queue for testing
# SF2866 Applied Systems Engineering
# Team Gamma

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import seaborn as sns

from person import Person
from test_queue import TestQueue
from model_id_state import ModelIdState


class Model:
    def __init__(self, duration=100, timeStep=1,  # days
                 susceptible=1000, infected=50, queued=0, removed=0,  # initial
                 rateSI=0.1,  # per timeStep
                 servers=5, serverMu=1, timeForTest=1,  # serverMu in days
                 pSymptomatic=.8, tSymptomatic=2, tRecovery=14,  # p-probability, t-time in  days
                 balking=None, reneging=None
                 ):
        self.Duration = duration
        self.TimeStep = timeStep
        self.NTimeSteps = int(duration/timeStep)
        self.InitialSusceptible = susceptible
        self.InitialInfected = infected
        self.InitialQueued = queued
        self.InitialRemoved = removed
        self.RateSI = rateSI

        self.Servers = servers/timeStep
        self.ServerMu = serverMu/timeStep

        self.PSymptomatic = pSymptomatic
        self.TSymptomatic = tSymptomatic/timeStep
        self.TRecovery = tRecovery/timeStep

        self.TotalIndividuals = susceptible + infected + removed
        self.Results = None
        self.HasModelRun = False

        self.People = [Person("S", pSymptomatic, tSymptomatic, tRecovery)
                       for i in range(susceptible)] \
            + [Person("I", pSymptomatic, tSymptomatic, tRecovery)
               for i in range(infected)] \
            + [Person("Q", pSymptomatic, tSymptomatic, tRecovery)
               for i in range(infected)] \
            + [Person("R", pSymptomatic, tSymptomatic, tRecovery)
               for i in range(removed)]

    def run(self):
        ts = list(range(0, self.Duration, self.TimeStep))

        for person in self.People:
            person.Advance(0)
        state = ModelIdState(self)
        queue = TestQueue(self.Servers, self.ServerMu)

        results = {"Time": ts,
                   "Susceptible": [len(state.SusceptibleIDs)],
                   "Infected": [len(state.InfectedIDs)],
                   "InfectedInfective": [len(state.InfectedInfectiveIDs)],
                   "InfectedSymptomatic": [len(state.InfectedSymptomaticIDs)],
                   "InfectedQueued": [len(state.InfectedQueuedIDs)],
                   "InfectedIsolated": [len(state.InfectedIsolatedIDs)],
                   "Removed": [len(state.RemovedIDs)]}

        for t in ts[1:]:
            # Advance people
            for person in self.People:
                person.Advance(t)
            state.UpdateState(self)

            # Infect
            # TODO: Not np.ceil, use np.round to closes int (including 0)
            S_to_I_count = int(np.round((self.RateSI * len(state.SusceptibleIDs) * len(state.InfectedInfectiveIDs)) /
                                        self.TotalIndividuals))
            if S_to_I_count > 0:
                S_to_I_Ids = random.sample(state.SusceptibleIDs, S_to_I_count)
                for i in S_to_I_Ids:
                    self.People[i].Infect(t)
            state.UpdateState(self)

            # Queue
            for id, person in enumerate(self.People):
                if person.ShouldQueue:
                    person.Queue(t)
                    queue.Put(id)
            state.UpdateState(self)

            # Test
            for id in queue.PopForTimeStep(self.TimeStep):
                self.People[id].Test(t)

            self.__addResults(results, state)

        self.Results = pd.DataFrame.from_dict(results)
        self.HasModelRun = True

    def __addResults(self, results, state):
        results['Susceptible'].append(len(state.SusceptibleIDs))
        results['Infected'].append(len(state.InfectedIDs))
        results['InfectedInfective'].append(len(state.InfectedInfectiveIDs))
        results['InfectedSymptomatic'].append(
            len(state.InfectedSymptomaticIDs))
        results['InfectedQueued'].append(len(state.InfectedQueuedIDs))
        results['InfectedIsolated'].append(len(state.InfectedIsolatedIDs))
        results['Removed'].append(len(state.RemovedIDs))

    def plot(self, fileName='result.png', openFile=True, title='Result'):
        # TODO: https://python-graph-gallery.com/251-stacked-area-chart-with-seaborn-style/
        if not self.HasModelRun:
            print('Error: Please call Model.run() before plotting.')
            return

        plt.subplot(3, 1, 1)
        plt.plot(self.Results['Time'],
                 self.Results['InfectedQueued'], color='orange')
        plt.legend(['Queued'],
                   bbox_to_anchor=(1.1, 1), loc='right', ncol=1, fancybox=True, shadow=True)
        plt.ylabel('Queue')
        plt.title(title)

        plt.subplot(3, 1, 2)
        plt.plot(self.Results['Time'],
                 self.Results['Infected'], color='green')
        plt.plot(self.Results['Time'],
                 self.Results['InfectedInfective'], color='red')
        plt.plot(self.Results['Time'],
                 self.Results['InfectedSymptomatic'], color='orange')
        plt.plot(self.Results['Time'],
                 self.Results['InfectedQueued'], color='blue')
        plt.plot(self.Results['Time'],
                 self.Results['InfectedIsolated'], color='gray')
        plt.ylabel('Infective')
        plt.legend(['Total', 'Infective', 'Symptomatic', 'Queued', 'Isolated'],
                   bbox_to_anchor=(1.1, 1), loc='right', ncol=1, fancybox=True, shadow=True)

        plt.subplot(3, 1, 3)
        # TODO: Stacking plot
        plt.plot(self.Results['Time'],
                 self.Results['Susceptible'], color='green')
        plt.plot(self.Results['Time'],
                 self.Results['Infected'], color='red')
        plt.plot(self.Results['Time'],
                 self.Results['Removed'], color='gray')
        plt.plot(self.Results['Time'],
                 np.sum([self.Results['Susceptible'], self.Results['Infected'], self.Results['Removed']], axis=0), color='black')
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.legend(['Susceptible', 'Infected', 'Removed', 'Total'],
                   bbox_to_anchor=(1.1, 1), loc='right', ncol=1, fancybox=True, shadow=True)
        plt.savefig(fileName, dpi=300)
        plt.close()
        if openFile:
            os.startfile(fileName, 'open')
