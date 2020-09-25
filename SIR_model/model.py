# SIR Model with M|M|s testing-queue

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

from .person import Person
from .test_queue import TestQueue
from .model_id_state import ModelIdState
from .result import Result
from .file_opener import openFile


class Model:
    """SIR-model with M|M|s testing queue.
    """

    def __init__(self, duration=100,  # days
                 susceptible=1000, infected=50, removed=0,  # initial
                 rateSI=0.14,  # per timeStep
                 pSymptomatic=.8, tSymptomatic=5, tRecovery=14,  # p-probability, t-time in  days
                 pFalseSymptoms=0.01, tFalseRecovery=7,
                 servers=1, serverMu=1/10,  # serverMu: day/person
                 tTestResult=1, queuePrioritization='FIFO',
                 tReneging=2,  # days, after revovery, None for no reneging
                 seed=None  # Specify with int for consistent result
                 ):
        """Runs automatically when a model object is created.
        """
        self.Duration = int(duration)
        self.NTimeSteps = int(duration+1)

        self.InitialSusceptible = susceptible
        self.InitialInfected = infected
        self.InitialRemoved = removed
        self.TotalIndividuals = susceptible + infected + removed
        self.RateSI = rateSI

        self.PSymptomatic = pSymptomatic
        self.TSymptomatic = tSymptomatic
        self.TRecovery = tRecovery
        self.PFalseSymptoms = pFalseSymptoms
        self.TFalseRecovery = tFalseRecovery

        self.NServers = servers
        self.ServerMu = serverMu
        self.TTestResult = tTestResult
        self.QueuePrioritization = queuePrioritization
        self.TReneging = tReneging

        self.Results = None
        self.HasModelRun = False

        if seed != None:
            np.random.seed(seed)

        self.People = [Person("S", pSymptomatic, tSymptomatic, tRecovery, tFalseRecovery, tTestResult, tReneging)
                       for i in range(susceptible)] \
            + [Person("I", pSymptomatic, tSymptomatic, tRecovery, tFalseRecovery, tTestResult, tReneging)
               for i in range(infected)] \
            + [Person("R", pSymptomatic, tSymptomatic, tRecovery, tFalseRecovery, tTestResult, tReneging)
               for i in range(removed)]

    def run(self):
        """Executes the simulation.
        """
        for person in self.People:
            person.advance(0)
        queue = TestQueue(self.NServers, self.ServerMu,
                          self.QueuePrioritization)
        state = ModelIdState(self.People, queue)

        ts = np.linspace(0, self.Duration, self.NTimeSteps)
        self.StartTime = 0
        self.EndTime = self.Duration
        results = Result({"Time": ts,
                          "ExpectedWaitTestResult": [self.TTestResult for i in range(len(ts))],
                          "ExpectedWaitService": [self.ServerMu for i in range(len(ts))]})
        self.__addResults(results, state)

        for t in ts[1:]:
            # Advance people
            for person in self.People:
                person.advance(t)
            state.updateState(self.People, queue)

            # Infect
            S_to_I_count = int(np.round((self.RateSI * len(state.SusceptibleIDs) * len(state.InfectedInfectiveUnisolatedIDs)) /
                                        self.TotalIndividuals))
            if S_to_I_count > 0:
                S_to_I_Ids = random.sample(state.SusceptibleIDs, S_to_I_count)
                for i in S_to_I_Ids:
                    self.People[i].infect(t)
            state.updateState(self.People, queue)

            # False symptoms
            S_to_FalseSymptoms_count = int(
                np.round(len(state.SusceptibleNotQueuedIDs)*self.PFalseSymptoms))
            if S_to_FalseSymptoms_count > 0:
                S_to_FalseSymptoms_Ids = random.sample(
                    state.SusceptibleNotQueuedIDs, S_to_FalseSymptoms_count)
                for i in S_to_FalseSymptoms_Ids:
                    self.People[i].falseSymptomsInfect(t)
            state.updateState(self.People, queue)

            # Queue
            for i, person in enumerate(self.People):
                if person.ShouldQueue:
                    person.queue(t)
                    queue.put(i)
            state.updateState(self.People, queue)

            # Test
            for i in queue.simulateDay():
                self.People[i].test(t)
            state.updateState(self.People, queue)

            # Renegade
            idsToRenegade = set()
            for i, person in enumerate(self.People):
                if person.ShouldRenegade:
                    idsToRenegade.add(i)
                    person.renegade(t)
            queue.renegade(idsToRenegade)
            state.updateState(self.People, queue)

            self.__addResults(results, state)

        self.Results = pd.DataFrame.from_dict(results.dictionary)
        self.HasModelRun = True

    def __addResults(self, results, state):
        """Iterates over the current state and sets appends a value to the corresponding result array.
        """
        results['Susceptible'].append(len(state.SusceptibleIDs))
        results['Infected'].append(len(state.InfectedIDs))
        results['Removed'].append(len(state.RemovedIDs))

        results['InfectedAsymptomaticUnisolated'].append(
            len(state.InfectedAsymptomaticUnisolatedIDs))
        results['InfectedSymptomaticUnisolated'].append(
            len(state.InfectedSymptomaticUnisolatedIDs))
        results['InfectedIsolated'].append(len(state.InfectedIsolatedIDs))
        results['InfectedInfectiveUnisolated'].append(
            len(state.InfectedInfectiveUnisolatedIDs))

        results['Queued'].append(len(state.QueuedIDs))
        results['SusceptibleQueued'].append(len(state.SusceptibleQueuedIDs))
        results['InfectedQueued'].append(len(state.InfectedQueuedIDs))
        results['RemovedQueued'].append(len(state.RemovedQueuedIDs))

        results['ExpectedWaitQueue'].append(state.ExpectedWaitQueue)
        results['ExpecteWaitTotal'].append(
            self.TTestResult + self.ServerMu + state.ExpectedWaitQueue)

    def oneplot(self):
        return self.subplots(1, 1)

    def subplots(self, nrows, ncols):
        sns.set_theme(style="darkgrid")
        fig, axs = plt.subplots(nrows, ncols)

        return fig, axs

    def plot(self, fileName='result.png', shouldOpenFile=True, title='SIR-model with M|M|s testing queue'):
        """Default plot of the result.
        """
        self.__plot(fileName, shouldOpenFile, title)

    def queueDistributionPlot(self, fileName='result_queue_distribution.png', shouldOpenFile=True, title='Queue distribution'):
        """Plot of the queue distribution.
        """
        self.__plot(fileName, shouldOpenFile, title, True)

    def __assertModelHasRun(self):
        if not self.HasModelRun:
            raise Exception('Call Model.run() before plotting.')

    def __plot(self, fileName='result.png', shouldOpenFile=True, title='SIR-model with M|M|s testing queue', queueDistributionPlot=False):
        self.__assertModelHasRun()
        sns.set_theme(style="darkgrid")

        fig, axs = plt.subplots(3, 1)
        if queueDistributionPlot:
            self.plotQueueDistribution(axs[0])
        else:
            self.plotExpectedWaitTime(axs[0])
        axs[0].set_title(title)
        self.plotInfected(axs[1])
        self.removeTicksX(axs[1])
        self.plotSIR(axs[2])
        self.removeTicksX(axs[2])

        fig.savefig(fileName, dpi=300)

        if shouldOpenFile:
            openFile(fileName)

    def plotExpectedWaitTime(self, ax):
        self.__assertModelHasRun()

        if self.NServers == 0:
            props = dict(boxstyle='round', facecolor='white', alpha=1)
            ax.text(.5, .5, r'$\infty$',
                    transform=ax.transAxes, fontsize=20,
                    verticalalignment='top', bbox=props,
                    ha='center', va='center')
            ax.set_ylabel(r'$E[T_{wait}]$ / days')
            ax.set_xticks([])
            ax.set_yticks([])
            return

        ax.stackplot(self.Results['Time'],
                     [self.Results['ExpectedWaitTestResult'],
                      self.Results['ExpectedWaitService'],
                      self.Results['ExpectedWaitQueue']],
                     labels=['Test result', 'Service', 'Queue'],
                     colors=['cadetblue', 'darkkhaki', 'khaki'])
        ax.set_xlabel('days')
        ax.set_ylabel(r'$E[T_{wait}]$ / days')
        ax.set_xlim(self.StartTime, self.EndTime)
        if max(self.Results['ExpecteWaitTotal']) < 1 or self.NServers == 0:
            ax.set_ylim(0, 1)
        else:
            ax.set_ylim(0)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1],
                  bbox_to_anchor=(1.1, 1), loc='right',
                  ncol=1, fancybox=True, shadow=True)

    def plotQueueDistribution(self, ax):
        self.__assertModelHasRun()

        ax.stackplot(self.Results['Time'],
                     [self.Results['InfectedQueued'],
                      self.Results['SusceptibleQueued'],
                      self.Results['RemovedQueued']],
                     labels=['Infected', 'Susceptible',  'Removed'],
                     colors=['salmon', 'lightgreen', 'dimgray'])
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1],
                  bbox_to_anchor=(1.1, 1), loc='right',
                  ncol=1, fancybox=True, shadow=True)
        ax.set_xlabel('days')
        ax.set_ylabel('queued')
        ax.set_xlim(self.StartTime, self.EndTime)
        if max(self.Results['Queued']) < 1:
            ax.set_ylim(0, 1)
        else:
            ax.set_ylim(0)

    def plotInfected(self, ax):
        self.__assertModelHasRun()

        ax.stackplot(self.Results['Time'],
                     [self.Results['InfectedAsymptomaticUnisolated'],
                      self.Results['InfectedSymptomaticUnisolated'],
                      self.Results['InfectedIsolated']],
                     labels=['Asymptomatic', 'Symptomatic', 'Isolated'],
                     colors=['rosybrown', 'indianred', 'dimgray'])
        ax.set_xlabel('days')
        ax.set_ylabel('infected')
        ax.set_xlim(self.StartTime, self.EndTime)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1],
                  bbox_to_anchor=(1.1, 1), loc='right',
                  ncol=1, fancybox=True, shadow=True)

    def plotSIR(self, ax):
        self.__assertModelHasRun()

        ax.stackplot(self.Results['Time'],
                     [self.Results['Infected'], self.Results['Susceptible'],
                      self.Results['Removed']], labels=['Infected', 'Susceptible', 'Removed'],
                     colors=['salmon', 'lightgreen', 'dimgray'])
        ax.set_xlabel('days')
        ax.set_ylabel('population')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1],
                  bbox_to_anchor=(1.1, 1), loc='right',
                  ncol=1, fancybox=True, shadow=True)
        ax.set_xlim(self.StartTime, self.EndTime)
        ax.set_ylim(0, self.TotalIndividuals)

    def removeTicksX(self, ax):
        ax.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False)
        ax.set_xlabel(None)

    def removeTicksY(self, ax):
        ax.tick_params(
            axis='y',
            which='both',
            left=False,
            right=False,
            labelleft=False)
        ax.set_ylabel(None)
