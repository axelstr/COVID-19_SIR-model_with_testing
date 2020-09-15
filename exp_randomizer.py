import numpy as np


class ExpRandomizer:
    def __init__(self):
        pass

    def fromMean(self, mean):
        return np.random.exponential(1/mean)
