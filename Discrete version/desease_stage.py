from enum import Enum


class DeseaseStage:

    def __init__(self, stage="S"):
        self.Stage = stage

        if stage == "I":
            self.InfectiveAt = 0
            self.SymptomaticAt = 0
        else:
            self.InfectiveAt = -1
            self.SymptomaticAt = -1

    def SetStage(self, stage, becomesInfectiveAt, showsSymptomsAt):
        self.Stage = stage
        self.BecomesInfectiveAt = becomesInfectiveAt
        self.SymptomaticAt = showsSymptomsAt

    # def advanceSymptoms(self, t):
    #     if self.Stage == "S":
    #         pass  # TODO: Do random cold symptoms
    #     elif self.Stage == "I":
    #         if self.SymptomaticAt >= 0 & t > self.SymptomaticAt:
    #             self.IsShowingSymptoms = True
    #     else:
    #         pass  # TODO: Do random cold symptoms depending on no times tested
