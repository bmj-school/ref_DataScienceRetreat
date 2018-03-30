import numpy as np


class Perceptron(object):
    def __init__(self):
        self.theta = None

    def fit(self, X, y):
        """
        Learns parameter vector self.theta from data X and binary labels y.

        y should have -1 for negative class and +1 for positive.
        X will be augmented with an intercept term before fitting.
        """
        assert X.shape[0] == y.shape[0]

        intercept = np.ones((X.shape[0], 1))
        X = np.concatenate((X, intercept), axis=1)
        raise NotImplementedError
