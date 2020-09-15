import numpy as np


class ExpRandomizer:
    """Randomizes random exponentially distributed numbers.
    """

    def __init__(self):
        pass

    def fromMean(self, mean):
        """Randomizes with the given mean as expected value.
        """
        return np.random.exponential(1/mean)
