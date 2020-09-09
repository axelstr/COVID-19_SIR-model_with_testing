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
from model_id_state import ModelIdState


class Model:
    def __init__(self, duration=365, timeStep=1, susceptible=10000000, infected=50, removed=0, rateSI=0.05, rateIR=0.01):
        self.Duration = duration
        self.TimeStep = timeStep
        self.InitialSusceptible = susceptible
        self.InitialInfected = infected
        self.InitialRemoved = removed
        self.RateSI = rateSI
        self.RateIR = rateIR
        self.TotalIndividuals = susceptible + infected + removed
        self.Results = None
        self.HasModelRun = False
        self.People = [Person("S") for i in range(susceptible)] \
            + [Person("I") for i in range(infected)] \
            + [Person("R") for i in range(removed)]

    def run(self):
        ts = list(range(0, self.Duration, self.TimeStep))

        state = ModelIdState(self)

        results = {"Time": ts,
                   "Susceptible": [len(state.SusceptibleIds)],
                   "Infected": [len(state.InfectedIds)],
                   "InfectedAndInfective": [len(state.InfectedAndInfectiveIds)],
                   "InfectedAndSymptomatic": [len(state.InfectedAndSymtomsIds)],
                   "Removed": [len(state.RemovedIds)]}

        for t in ts[1:]:
            # Queue infected
            # TODO: Implement

            # Isolate positive tests
            # TODO: Implement
            # Isolate_Ids = [i for i in state.InfectedAndInfectiveIds
            #                if self.People[i].TestResult.AvailableTime > t and self.People[i].TestResult.IsPositive == True]
            # for i in Isolate_Ids:
            #     self.People[i].SetStage("R")
            # state.UpdateState(self, t)

            # Infect and remove
            S_to_I_count = int((self.RateSI * len(state.SusceptibleIds) * len(state.InfectedAndInfectiveIds)) /
                               self.TotalIndividuals)
            if S_to_I_count > 0:
                S_to_I_Ids = random.sample(state.SusceptibleIds, S_to_I_count)
                for i in S_to_I_Ids:
                    self.People[i].SetStage("I", t+4, t+7)

            I_to_R_count = int(len(state.InfectedIds) * self.RateIR)
            if I_to_R_count > 0:
                I_to_R_Ids = random.sample(state.InfectedIds, I_to_R_count)
                for i in I_to_R_Ids:
                    self.People[i].SetStage("R")

            state.UpdateState(self, t)

            self.__addResults(results, state)

        self.Results = pd.DataFrame.from_dict(results)
        self.HasModelRun = True

    def plot(self, fileName='result.png', openFile=True):
        if self.HasModelRun == False:
            print('Error: Model has not run. Please call SIR.run()')
            return
        plt.plot(self.Results['Time'],
                 self.Results['Susceptible'], color='blue')
        plt.plot(self.Results['Time'],
                 self.Results['Infected'], color='red')
        plt.plot(self.Results['Time'],
                 self.Results['Removed'], color='green')
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.legend(['Susceptible', 'Infected', 'Removed'], prop={
                   'size': 10}, loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3, fancybox=True, shadow=True)
        # plt.title(r'$\beta = {0}, \gamma = {1}$'.format(
        #     self.RateSI, self.RateIR))
        plt.savefig(fileName, dpi=300)
        plt.close()
        if openFile:
            os.startfile(fileName, 'open')

    def __addResults(self, results, state):
        results['Susceptible'].append(len(state.SusceptibleIds))
        results['Infected'].append(len(state.InfectedIds))
        results['InfectedAndInfective'].append(
            len(state.InfectedAndInfectiveIds))
        results['InfectedAndSymptomatic'].append(
            len(state.InfectedAndSymtomsIds))
        results['Removed'].append(len(state.RemovedIds))

    def __advancePeople(self, t):
        for person in self.People:
            person.Advance(t)
