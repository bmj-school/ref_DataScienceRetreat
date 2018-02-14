import numpy as np


class FeatureMappedPerceptron(object):
    def __init__(self, phi):
        """
        Explicit feature mapped version of Perceptron algorithm.
        :param phi: Callable, function from original feature space to mapped feature space.
        """
        assert callable(phi)
        self.phi = phi
        self.theta = None

    def predict(self, x):
        raise NotImplementedError

    def fit(self, X, y):
        """
        Learns parameter vector self.theta from data X and binary labels y.

        y should have -1 for negative class and +1 for positive.
        X will be augmented with an intercept term before fitting.
        """
        assert X.shape[0] == y.shape[0]

        intercept = np.ones((X.shape[0], 1))
        X = np.concatenate((X, intercept), axis=1)

        d = self.phi(X[0, :]).shape[0]
        self.theta = np.random.randn(d, 1)

        raise NotImplementedError
