class ModelIdState:

    def __init__(self, people, queue):
        self.UpdateState(people, queue)

    def UpdateState(self, people, queue):
        self.SusceptibleIDs = [i for (i, p) in
                               enumerate(people) if p.Stage == "S"]
        self.InfectedIDs = [i for (i, p) in
                            enumerate(people) if p.Stage == "I"]
        self.RemovedIDs = [i for (i, p) in
                           enumerate(people) if p.Stage == "R"]
        self.InfectedInfectiveIDs = [i for (i, p) in
                                     enumerate(people) if p.Stage == "I" and p.IsInfective]
        self.InfectedAsymptomaticIDs = [i for (i, p) in
                                        enumerate(people) if p.Stage == "I" and (not p.IsSymptomatic)]
        self.InfectedSymptomaticUnisolatedIDs = [i for (i, p) in
                                                 enumerate(people) if p.Stage == "I" and p.IsSymptomatic and (not p.IsIsolated)]
        self.InfectedSymptomaticIDs = [i for (i, p) in
                                       enumerate(people) if p.Stage == "I" and p.IsSymptomatic]
        self.QueuedIDs = [i for (i, p) in
                          enumerate(people) if p.Stage == "I" and p.IsQueued]
        self.InfectedIsolatedIDs = [i for (i, p) in
                                    enumerate(people) if p.Stage == "I" and p.IsIsolated]
        self.ExpectedWaitingTime = queue.GetExpectedWaitingTime()

    def Control(self):
        if not (len(self.InfectedIDs == (len(self.InfectedAsymptomaticIDs) + len(self.InfectedSymptomaticUnisolatedIDs) + len(self.InfectedIsolatedIDs)))):
            raise Exception(
                "Infected subgroups does not add up to total infected.")
