class Person:
    """Person object.
    """

    def __init__(self, deseaseStage="S"):
        self.Stage = deseaseStage
        if deseaseStage == "I":
            self.Infect(0)

        self.IsInfective = False
        self.IsSymptomatic = False
        self.ShouldQueue = False
        self.IsQueued = False
        self.IsIsolated = False

    def Advance(self, t):

        if self.Stage == "I":
            if t >= self.SymptomaticAt:
                _ = 1
            if (not self.IsInfective) and t >= self.InfectiveAt:
                self.IsInfective = True
            if (not self.IsSymptomatic) and t >= self.SymptomaticAt:
                self.IsSymptomatic = True
                if (not self.ShouldQueue):
                    (self.ShouldQueue) = True
            if t >= self.RecoverAt:
                self.Recover(t)

    def Infect(self, t):
        self.Stage = "I"
        self.InfectiveAt = t+0
        self.SymptomaticAt = t+2
        self.RecoverAt = t+14
        # TODO: Randomize, some never gets symptomatic

    def Queue(self, t):
        self.ShouldQueue = False
        self.IsQueued = True
        self.QueuedAt = t

    def Recover(self, t):
        self.Stage = "R"
        self.IsInfective = False
        self.IsSymptomatic = False
        self.IsQueued = False
        self.IsIsolated = False

    def Test(self, t):
        if self.Stage == "S":
            # TODO: Implement
            pass

        if self.Stage == "I":
            self.IsInfective = False  # Can't infect since isolated
            self.IsQueued = False
            self.IsIsolated = True
        if self.Stage == "R":
            # TODO: Implement
            pass
