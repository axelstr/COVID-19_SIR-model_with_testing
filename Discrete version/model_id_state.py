class ModelIdState:

    def __init__(self, model):
        self.UpdateState(model, 0)

    def UpdateState(self, model, t):
        self.SusceptibleIds = [i for (i, p) in enumerate(
            model.People) if p.DeseaseStage.Stage == "S"]
        self.InfectedIds = [i for (i, p) in enumerate(
            model.People) if p.DeseaseStage.Stage == "I"]
        self.InfectedAndInfectiveIds = [i for (i, p) in enumerate(
            model.People) if p.DeseaseStage.Stage == "I" and p.DeseaseStage.InfectiveAt >= t]
        self.InfectedAndSymtomsIds = [i for (i, p) in enumerate(
            model.People) if p.DeseaseStage.Stage == "I" and p.DeseaseStage.SymptomaticAt >= t]
        self.RemovedIds = [i for (i, p) in enumerate(
            model.People) if p.DeseaseStage.Stage == "R"]
