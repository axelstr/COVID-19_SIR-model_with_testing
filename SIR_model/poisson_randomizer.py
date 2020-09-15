import numpy as np


class PoissonRandomizer:
    """Randomizes random exponentially distributed numbers.
    """

    def __init__(self):
        pass

    def fromMean(self, mean):
        """Randomizes with the given mean as expected value.
        """
        return np.random.poisson(mean)
