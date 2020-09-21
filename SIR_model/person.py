from .poisson_randomizer import PoissonRandomizer
from .exp_randomizer import ExpRandomizer
import numpy as np


class Person:
    """Person object.
    """

    def __init__(self, deseaseStage, pSymptomatic, tSymptomatic, tRecovery, tFalseRecovery, tTestResult, tRenegade):
        self.PoissonRandomizer = PoissonRandomizer()
        self.ExpRandomizer = ExpRandomizer()

        self.PSymptomatic = pSymptomatic
        self.TSymptomatic = tSymptomatic
        self.TRecovery = tRecovery
        self.TFalseRecovery = tFalseRecovery
        self.TTestResult = tTestResult
        self.TRenegade = tRenegade

        self.IsInfective = False
        self.WillBeSymptomatic = False
        self.IsSymptomatic = False
        self.ShouldQueue = False
        self.IsQueued = False
        self.ShouldRenegade = False
        self.WillIsolate = False
        self.IsIsolated = False
        self.HasTestedPositive = False
        self.IsFalseSymptomatic = False

        self.InfectiveAt = None
        self.SymptomaticAt = None
        self.RecoverAt = None
        self.FalseRecoverAt = None
        self.IsolateAt = None
        self.RenegadesAt = None

        self.Stage = deseaseStage
        if deseaseStage == "I":
            self.infect(0)

    def advance(self, t):
        """Advances the person to the current timestep.
        """
        if self.IsFalseSymptomatic:
            if t >= self.FalseRecoverAt:
                self.falseRecover(t)

        if self.Stage == "I":
            if (not self.IsInfective) and t >= self.InfectiveAt:
                self.IsInfective = True
                self.InfectiveAt = None
            if self.WillBeSymptomatic and (not self.IsSymptomatic) and t >= self.SymptomaticAt:
                self.IsSymptomatic = True
                self.WillBeSymptomatic = False
                self.ShouldQueue = True
                self.RenegadesAt = None
                self.ShouldRenegade = False
            if self.WillIsolate and (t >= self.IsolateAt):
                self.isolate(t)
            if t >= self.RecoverAt:
                self.recover(t)

        if self.IsQueued and (not self.ShouldRenegade) and (self.TRenegade != None):
            if (self.RenegadesAt == None):
                if (not self.IsSymptomatic) and (not self.IsFalseSymptomatic):
                    self.RenegadesAt = t + \
                        self.ExpRandomizer.fromMean(self.TRenegade)
            else:
                if t >= self.RenegadesAt:
                    self.ShouldRenegade = True
                    self.RenegadesAt = None

    def infect(self, t):
        """Infects a person with covid-19.
        """
        self.Stage = "I"
        self.InfectiveAt = t+0
        self.RecoverAt = t+self.PoissonRandomizer.fromMean(self.TRecovery)

        self.WillBeSymptomatic = np.random.rand() <= self.PSymptomatic
        if self.WillBeSymptomatic:
            self.SymptomaticAt = t + \
                self.PoissonRandomizer.fromMean(self.TSymptomatic)

    def falseSymptomsInfect(self, t):
        """Infects a person with false symtpoms (non-covid related illness).
        """
        self.ShouldQueue = True
        self.IsFalseSymptomatic = True
        self.FalseRecoverAt = t + \
            self.PoissonRandomizer.fromMean(self.TFalseRecovery)

    def queue(self, t):
        """Tells a person object that it is queued.
        """
        self.ShouldQueue = False
        self.IsQueued = True
        self.QueuedAt = t

    def renegade(self, t):
        """Renagades a person.
        """
        self.IsQueued = False
        self.ShouldRenegade = False

    def test(self, t):
        """Tests a person for covid-19. Schedules isolation when result is available.
        """
        if self.Stage == "S":
            self.IsQueued = False

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

    def isolate(self, t):
        self.IsIsolated = True
        self.WillIsolate = False
        self.IsolateAt = None

    def recover(self, t):
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

    def falseRecover(self, t):
        """Recovers a person from false symptomps.
        """
        self.IsFalseSymptomatic = False
