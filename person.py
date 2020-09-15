from poisson_randomizer import PoissonRandomizer
import numpy as np


class Person:
    """Person object.
    """

    def __init__(self, deseaseStage, pSymptomatic, tSymptomatic, tRecovery, tTestResult):
        self.PoissonRandomizer = PoissonRandomizer()
        self.PSymptomatic = pSymptomatic
        self.TSymptomatic = tSymptomatic
        self.TRecovery = tRecovery
        self.TTestResult = tTestResult

        self.Stage = deseaseStage
        if deseaseStage == "I":
            self.Infect(0)

        self.IsInfective = False
        self.IsSymptomatic = False
        self.ShouldQueue = False
        self.IsQueued = False
        self.WillIsolate = False
        self.IsIsolated = False

    def Advance(self, t):
        if self.Stage == "I":
            if (not self.IsInfective) and t >= self.InfectiveAt:
                self.IsInfective = True
                self.InfectiveAt = None
            if self.WillBeSymptomatic and (not self.IsSymptomatic) and t >= self.SymptomaticAt:
                self.IsSymptomatic = True
                self.WillBeSymptomatic = False
                self.ShouldQueue = True
            if self.WillIsolate and (t >= self.IsolateAt):
                self.IsIsolated = True
                self.WillIsolate = False
                self.IsolateAt = None
            if t >= self.RecoverAt:
                self.Recover(t)

    def Infect(self, t):
        self.Stage = "I"
        self.InfectiveAt = t+0
        self.RecoverAt = t+self.PoissonRandomizer.fromMean(self.TRecovery)

        self.WillBeSymptomatic = np.random.rand() <= self.PSymptomatic
        if self.WillBeSymptomatic:
            self.SymptomaticAt = t + \
                self.PoissonRandomizer.fromMean(self.TSymptomatic)

    def Queue(self, t):
        self.ShouldQueue = False
        self.IsQueued = True
        self.QueuedAt = t

    def Recover(self, t):
        self.Stage = "R"
        self.IsInfective = None
        self.IsSymptomatic = None
        self.WillIsolate = None
        self.IsQueued = None
        self.IsIsolated = None
        self.IsInfective = None
        self.IsSymptomatic = None

    def Test(self, t):
        # TODO: Delay with time to get result
        if self.Stage == "I":
            if self.TTestResult == 0:
                self.IsQueued = False
                self.IsIsolated = True
            else:
                self.IsQueued = False
                self.WillIsolate = True
                self.IsolateAt = t + self.TTestResult
