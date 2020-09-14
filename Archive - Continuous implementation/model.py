# SIR Model with M|M|s queue for testing
# SF2866 Applied Systems Engineering
# Team Gamma

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import seaborn as sns

from matplotlib import rc
# rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# for Palatino and other serif fonts use:
# rc('font', **{'family': 'serif', 'serif': ['Palatino']})
rc('text', usetex=True)


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
                                            self.TRecovery)
        self.PdfQtoR = self.__getPoissonPdf(self.NTimeSteps,
                                            self.TRecovery)

        self.TotalIndividuals = susceptible + infected + removed
        self.Results = None
        self.HasModelRun = False

    def run(self):
        ts = list(range(0, self.Duration, self.TimeStep))
        zeros = [0 for _ in range(1, self.NTimeSteps)]
        S = np.array([self.InitialSusceptible] + zeros, dtype='f')
        I_nq = np.array([self.InitialInfected] + zeros, dtype='f')
        I_nq_byInfectedTime = np.array(
            [self.InitialInfected] + zeros, dtype='f')
        I_q = np.array([self.InitialQueued] + zeros, dtype='f')
        I_q_byInfectedTime = np.array([self.InitialQueued] + zeros, dtype='f')
        R = np.array([self.InitialRemoved] + zeros, dtype='f')

        for i in range(0, self.NTimeSteps-1):
            # Euler forward
            S_to_I_nq = self.__S_to_I(i, S, I_nq, I_q)
            I_nq_to_R = self.__I_nq_to_R(i, I_nq_byInfectedTime)
            I_q_to_R = self.__I_q_to_R(i, I_q_byInfectedTime)

            # Step forward
            S[i+1] = S[i] - S_to_I_nq
            I_nq[i+1] = I_nq[i] + S_to_I_nq - I_nq_to_R
            I_nq_byInfectedTime[i+1] = S_to_I_nq
            I_q[i+1] = I_q[i] - I_q_to_R
            R[i+1] = R[i] + I_nq_to_R + I_q_to_R

            # Queue infected that shows symptomps
            n = min(i+1, len(self.PdfItoQ))
            for k in range(n):
                q = I_nq_byInfectedTime[i-k]*self.PdfItoQ[k]
                I_nq_byInfectedTime[i-k] -= q
                I_q_byInfectedTime[i-k] += q
                I_nq[i+1] -= q
                I_q[i+1] += q

        self.Results = pd.DataFrame.from_dict({"Time": ts,
                                               "Susceptible": S,
                                               "Infected": np.sum([I_nq, I_q], axis=0),
                                               "Queued": I_q,
                                               "Removed": R})
        self.HasModelRun = True

    def __S_to_I(self, i, S, I, I_Q):
        f = (self.RateSI * S[i] * (I[i]+I_Q[i])) \
            / self.TotalIndividuals
        return f

    def __I_nq_to_R(self, i, I_byInfectedTime):
        f = self.__conv(I_byInfectedTime, self.PdfItoR, i)
        return f

    def __I_q_to_R(self, i, I_Q_byInfectedTime):
        f = self.__conv(I_Q_byInfectedTime, self.PdfQtoR, i)
        return f

    def __conv(self, array, pdf, index):
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
            pdf.append(pow*exp/factorial)
            pow *= mean
            factorial *= i

        return np.array(pdf, dtype='f')*totalProbability

    def plot(self, fileName='result.png', openFile=True, title='Result'):
        if not self.HasModelRun:
            print('Error: Please call Model.run() before plotting.')
            return

        plt.subplot(2, 1, 1)
        plt.plot(self.Results['Time'],
                 self.Results['Queued'], color='orange')
        plt.legend(['Queued'], prop={
                   'size': 10}, loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3, fancybox=True, shadow=True)
        plt.ylabel('Population')
        plt.title(title)

        plt.subplot(2, 1, 2)
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
        plt.legend(['Susceptible', 'Infected', 'Removed', 'Total'], prop={
                   'size': 10}, loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3, fancybox=True, shadow=True)
        plt.savefig(fileName, dpi=300)
        plt.close()
        if openFile:
            os.startfile(fileName, 'open')
