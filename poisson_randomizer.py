import numpy as np


class PoissonRandomizer:
    def __init__(self):
        pass

    def fromMean(self, mean):
        return np.random.poisson(mean)
