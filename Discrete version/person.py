from test_result import TestResult
from desease_stage import DeseaseStage


class Person:

    def __init__(self, deseaseStage="S"):
        self.DeseaseStage = DeseaseStage(deseaseStage)
        self.TestResult = TestResult()

    # def Advance(self, t):

    def SetStage(self, stage, becomesInfectiveAt=-1, showsSymptomsAt=-1):
        self.DeseaseStage.SetStage(stage, becomesInfectiveAt, showsSymptomsAt)
