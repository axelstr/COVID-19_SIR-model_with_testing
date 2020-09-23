from .exp_randomizer import ExpRandomizer

import numpy as np


class Server:
    def __init__(self, mu, employmentRate):
        self.ExpRandomizer = ExpRandomizer()
        self.Mu = mu
        self.EmploymentRate = employmentRate
        self.DayWrapOption = "overtime-flex"
        self.InitialTime = 0
        self.ServedByFull = []
        self.ServedByFraction = []

    def simulateDay(self):
        t = self.InitialTime
        served = 0
        while t < self.EmploymentRate:
            served += 1
            t += self.ExpRandomizer.fromMean(self.Mu)
        if self.DayWrapOption == 'overtime':
            self.InitialTime = 0
        elif self.DayWrapOption == 'overtime-flex':
            self.InitialTime = t-self.EmploymentRate
        else:
            raise Exception(
                f"Invalid day-wrap option \"{self.DayWrapOption}\"")

        return served
