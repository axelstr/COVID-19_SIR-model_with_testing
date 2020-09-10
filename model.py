# SIR Model with M|M|s queue for testing
# SF2866 Applied Systems Engineering
# Team Gamma

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import seaborn as sns


class Model:
    def __init__(self, duration=100, timeStep=1,  # days
                 susceptible=1000, infected=50, queued=0, removed=0,  # initial
                 rateSI=0.1,  # per timeStep
                 servers=1000, serverMu=1, timeForTest=1,  # serverMu in days
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

        self.PdfItoQ = self.__getPoissonPdf(self.NTimeSteps,
                                            self.TSymptomatic,
                                            self.PSymptomatic)
        self.PdfItoR = self.__getPoissonPdf(self.NTimeSteps,
                                            self.TRecovery,
                                            1-self.PSymptomatic)
        self.PdfQtoR = self.__getPoissonPdf(self.NTimeSteps,
                                            self.TRecovery)

        self.TotalIndividuals = susceptible + infected + removed
        self.Results = None
        self.HasModelRun = False

    def run(self):
        ts = list(range(0, self.Duration, self.TimeStep))
        zeros = [0 for _ in range(1, self.NTimeSteps)]
        S = np.array([self.InitialSusceptible] + zeros, dtype='f')
        I = np.array([self.InitialInfected] + zeros, dtype='f')
        I_byInfectedTime = np.array([self.InitialInfected] + zeros, dtype='f')
        # I_left = np.array([self.InitialInfected] + zeros,
        #                   dtype='f')
        # Q = np.array([self.InitialQueued] + zeros, dtype='f')
        # Q_left = np.array([self.InitialQueued] + zeros, dtype='f')
        R = np.array([self.InitialRemoved] + zeros, dtype='f')

        for i in range(0, self.NTimeSteps-1):
            S_to_I = self.__S_to_I(i, S, I)
            # I_to_Q, Imoved = self.__I_to_Q(i, I_left)
            I_to_R = self.__I_to_R(i, I_byInfectedTime)
            # Q_to_R, Qmoved = self.__Q_to_R(i, I, Q, R, S)
            # Q_left = self.__removeMoved(Q_left, Qmoved)

            S[i+1] = S[i] - S_to_I
            I[i+1] = I[i] + S_to_I - I_to_R  # - I_to_Q
            I_byInfectedTime[i+1] = S_to_I
            # I_left[i+1] = I[i+1]
            # Q[i+1] = Q[i] + I_to_Q - Q_to_R
            # Q_left[i+1] = Q[i+1]
            R[i+1] = R[i] + I_to_R  # + Q_to_R

        self.Results = pd.DataFrame.from_dict({"Time": ts,
                                               "Susceptible": S,
                                               "Infected": I,
                                               #    "Queued": Q,
                                               "Removed": R})
        self.HasModelRun = True

    def __S_to_I(self, i, S, I):
        f = (self.RateSI * S[i] * (I[i])) \
            / self.TotalIndividuals
        return f

    def __I_to_Q(self, i, I_left):
        f = self.__conv(I_left, self.PdfItoQ, i)
        return f

    def __I_to_R(self, i, I_left):
        f = self.__conv(I_left, self.PdfItoR, i)
        return f

    def __Q_to_R(self, i, I, Q, R, S):
        f = self.__conv(Q, self.PdfItoR, i)
        return f

    def __conv(self, array, pdf, index):
        print(sum(pdf))
        n = min(index+1, len(pdf), len(array))
        s = 0
        for k in range(0, n):
            s += array[index-k]*pdf[k]

        if s > sum(array):
            _ = 1

        return s

    def __removeMoved(self, array, moved):
        for i in range(min(len(array), len(moved))):
            array[i] = array[i] - moved[i]
        return array

    def __getPoissonPdf(self, arrayLength, mean, totalProbability=1):
        pow = 1
        factorial = 1
        exp = np.exp(-mean)
        pdf = [pow*exp/factorial]
        # Multiplication overflow, value < 1e-50
        arrayLength = min(50, arrayLength)

        for i in range(1, arrayLength):
            pdf.append(pow*exp/factorial*totalProbability)
            pow *= mean
            factorial *= i

        return np.array(pdf)

    def plot(self, fileName='result.png', openFile=True, title='Result'):
        if not self.HasModelRun:
            print('Error: Please call Model.run() before plotting.')
            return
        plt.plot(self.Results['Time'],
                 self.Results['Susceptible'], color='green')
        plt.plot(self.Results['Time'],
                 self.Results['Infected'], color='red')
        # plt.plot(self.Results['Time'],
        #          self.Results['Queued'], color='orange')
        plt.plot(self.Results['Time'],
                 self.Results['Removed'], color='gray')
        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.legend(['Susceptible', 'Infected', 'Removed'], prop={
                   'size': 10}, loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3, fancybox=True, shadow=True)
        plt.title(title)
        plt.savefig(fileName, dpi=300)
        plt.close()
        if openFile:
            os.startfile(fileName, 'open')
