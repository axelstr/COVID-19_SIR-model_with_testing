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
    def __init__(self, duration=100,  # days
                 susceptible=1000, infected=50, queued=0, removed=0,  # initial
                 rateSI=0.1,  # per timeStep
                 servers=5, serverMu=1, timeForTest=1,  # serverMu in days
                 pSymptomatic=.8, tSymptomatic=2, tRecovery=14,  # p-probability, t-time in  days
                 seed=None  # Specify for consistent result
                 ):
        self.Duration = int(duration)
        self.NTimeSteps = int(duration+1)

        self.InitialSusceptible = susceptible
        self.InitialInfected = infected
        self.InitialQueued = queued
        self.InitialRemoved = removed
        self.TotalIndividuals = susceptible + infected + removed
        self.RateSI = rateSI

        self.Servers = servers
        self.ServerMu = serverMu

        self.PSymptomatic = pSymptomatic
        self.TSymptomatic = tSymptomatic
        self.TRecovery = tRecovery

        self.Results = None
        self.HasModelRun = False

        if seed != None:
            np.random.seed(seed)

        self.People = [Person("S", pSymptomatic, tSymptomatic, tRecovery)
                       for i in range(susceptible)] \
            + [Person("I", pSymptomatic, tSymptomatic, tRecovery)
               for i in range(infected)] \
            + [Person("Q", pSymptomatic, tSymptomatic, tRecovery)
               for i in range(infected)] \
            + [Person("R", pSymptomatic, tSymptomatic, tRecovery)
               for i in range(removed)]

    def run(self):
        ts = np.linspace(0, self.Duration, self.NTimeSteps)

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
            for id in queue.PopForOneDay():
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
        startTime = 0
        endTime = max(self.Results['Time'])
        if not self.HasModelRun:
            print('Error: Please call Model.run() before plotting.')
            return

        sns.set_theme(style="darkgrid")

        # TODO: Plot expected wait time
        plt.subplot(3, 1, 1)
        plt.stackplot(self.Results['Time'],
                      [self.Results['InfectedQueued']],
                      labels=['Infected'],
                      colors=['salmon', 'lightgreen'])
        plt.legend(bbox_to_anchor=(1.1, 1), loc='right',
                   ncol=1, fancybox=True, shadow=True)
        plt.ylabel('Queued')
        plt.title(title)
        plt.xlim(startTime, endTime)
        plt.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False)

        plt.subplot(3, 1, 2)
        plt.stackplot(self.Results['Time'],
                      [self.Results['InfectedInfective'],
                       self.Results['InfectedIsolated']],
                      labels=['Infective', 'Isolated'],
                      colors=['salmon', 'dimgray'])
        plt.ylabel('Infected')
        plt.legend(bbox_to_anchor=(1.1, 1), loc='right',
                   ncol=1, fancybox=True, shadow=True)
        plt.xlim(startTime, endTime)
        plt.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False)

        plt.subplot(3, 1, 3)
        plt.stackplot(self.Results['Time'],
                      [self.Results['Infected'], self.Results['Susceptible'],
                       self.Results['Removed']], labels=['Infected', 'Susceptible', 'Removed'],
                      colors=['salmon', 'lightgreen', 'dimgray'])
        plt.xlabel('Time')
        plt.ylabel('SIR')
        plt.legend(bbox_to_anchor=(1.1, 1), loc='right',
                   ncol=1, fancybox=True, shadow=True)
        plt.xlim(startTime, endTime)
        plt.ylim(0, self.TotalIndividuals)
        plt.savefig(fileName, dpi=300)
        plt.close()
        if openFile:
            os.startfile(fileName, 'open')
