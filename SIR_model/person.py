from .poisson_randomizer import PoissonRandomizer
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
        self.WillBeSymptomatic = False
        self.IsSymptomatic = False
        self.ShouldQueue = False
        self.IsQueued = False
        self.WillIsolate = False
        self.IsIsolated = False
        self.HasTestedPositive = False

    def Advance(self, t):
        """Advances the person to the current timestep.
        """
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
        """Infects a person with covid-19.
        """
        self.Stage = "I"
        self.InfectiveAt = t+0
        self.RecoverAt = t+self.PoissonRandomizer.fromMean(self.TRecovery)

        self.WillBeSymptomatic = np.random.rand() <= self.PSymptomatic
        if self.WillBeSymptomatic:
            self.SymptomaticAt = t + \
                self.PoissonRandomizer.fromMean(self.TSymptomatic)

    def FalseSymptomsInfect(self, t):
        """Infects a person with false symtpoms (non-covid related illness).
        """
        self.ShouldQueue = True
        self.IsSymptomatic = True

    def Queue(self, t):
        """Tells a person object that it is queued.
        """
        self.ShouldQueue = False
        self.IsQueued = True
        self.QueuedAt = t

    def Recover(self, t):
        """Recovers a person from covid-19.
        """
        self.Stage = "R"
        self.IsInfective = None
        self.IsSymptomatic = None
        self.WillIsolate = None
        # self.IsQueued = None
        self.IsIsolated = None
        self.IsInfective = None
        self.IsSymptomatic = None

    def Test(self, t):
        """Tests a person for covid-19. Schedules isolation when result is available.
        """
        if self.Stage == "S":
            self.IsQueued = False
            self.IsSymptomatic = False

        elif self.Stage == "I":
            self.HasTestedPositive = True
            if self.TTestResult == 0:
                self.IsQueued = False
                self.IsIsolated = True
            else:
                self.IsQueued = False
                self.WillIsolate = True
                self.IsolateAt = t + self.TTestResult

        if self.Stage == "R":
            self.IsQueued = False
