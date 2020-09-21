class ModelIdState:
    """Object that tracks the current state of the list of people.
    """

    def __init__(self, people, queue):
        self.UpdateState(people, queue)

    def UpdateState(self, people, queue):
        self.SusceptibleIDs = [i for (i, p) in
                               enumerate(people) if p.Stage == "S"]
        self.InfectedIDs = [i for (i, p) in
                            enumerate(people) if p.Stage == "I"]
        self.QueuedIDs = [i for (i, p) in
                          enumerate(people) if p.IsQueued]
        self.RemovedIDs = [i for (i, p) in
                           enumerate(people) if p.Stage == "R"]

        self.SusceptibleNotQueuedIDs = [i for (i, p) in
                                        enumerate(people) if p.Stage == "S" and (not p.IsQueued)]
        self.SusceptibleQueuedIDs = [i for (i, p) in
                                     enumerate(people) if p.Stage == "S" and p.IsQueued]

        self.InfectedInfectiveIDs = [i for (i, p) in
                                     enumerate(people) if p.Stage == "I" and p.IsInfective]
        self.InfectedAsymptomaticUnisolatedIDs = [i for (i, p) in
                                                  enumerate(people) if p.Stage == "I" and (not p.IsSymptomatic) and (not p.IsIsolated)]
        self.InfectedSymptomaticUnisolatedIDs = [i for (i, p) in
                                                 enumerate(people) if p.Stage == "I" and p.IsSymptomatic and (not p.IsIsolated)]
        self.InfectedSymptomaticIDs = [i for (i, p) in
                                       enumerate(people) if p.Stage == "I" and p.IsSymptomatic]
        self.InfectedIsolatedIDs = [i for (i, p) in
                                    enumerate(people) if p.Stage == "I" and p.IsIsolated]
        self.InfectedInfectiveUnisolatedIDs = [i for (i, p) in
                                               enumerate(people) if p.Stage == "I" and p.IsInfective and (not p.IsIsolated)]

        self.CanShowFalseSymptomsIDs = [i for (i, p) in
                                        enumerate(people) if p.Stage != "I" and (not p.IsQueued) and (not p.HasTestedPositive)]

        self.SusceptibleQueuedIDs = [i for (i, p) in
                                     enumerate(people) if p.Stage == "S" and p.IsQueued]
        self.InfectedQueuedIDs = [i for (i, p) in
                                  enumerate(people) if p.Stage == "I" and p.IsQueued]
        self.RemovedQueuedIDs = [i for (i, p) in
                                 enumerate(people) if p.Stage == "R" and p.IsQueued]

        self.ExpectedWaitingTime = queue.GetExpectedWaitingTime()

        self.Control()

    def Control(self):
        totalInfected = len(self.InfectedIDs)
        asymptomatic = len(self.InfectedAsymptomaticUnisolatedIDs)
        symptomaticUnisolated = len(self.InfectedSymptomaticUnisolatedIDs)
        isolated = len(self.InfectedIsolatedIDs)
        s = asymptomatic + symptomaticUnisolated + isolated

        if not (totalInfected == s):
            raise Exception(
                "Infected subgroups does not add up to total infected.")
