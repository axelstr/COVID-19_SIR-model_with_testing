class ModelIdState:

    def __init__(self, model):
        self.UpdateState(model)

    def UpdateState(self, model):
        self.SusceptibleIDs = [i for (i, p) in
                               enumerate(model.People) if p.Stage == "S"]
        self.InfectedIDs = [i for (i, p) in
                            enumerate(model.People) if p.Stage == "I"]
        self.InfectedInfectiveIDs = [i for (i, p) in
                                     enumerate(model.People) if p.Stage == "I" and p.IsInfective]
        self.InfectedSymptomaticIDs = [i for (i, p) in
                                       enumerate(model.People) if p.Stage == "I" and p.IsSymptomatic]
        self.InfectedQueuedIDs = [i for (i, p) in
                                  enumerate(model.People) if p.Stage == "I" and p.IsQueued]
        self.InfectedIsolatedIDs = [i for (i, p) in
                                    enumerate(model.People) if p.Stage == "I" and p.IsIsolated]
        self.RemovedIDs = [i for (i, p) in
                           enumerate(model.People) if p.Stage == "R"]
