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
        return np.dot(self.theta.T, self.phi(x))

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
        theta_updated = True
        while theta_updated:
            theta_updated = False
            for i in range(X.shape[0]):
                x, yy = X[i, :], y[i]
                # if label yy and sign of decision function do not agree
                # sample x on wrong side of the hyperplane
                if yy * (np.dot(self.theta.T, self.phi(x))) <= 0:
                    # -y * theta.T * phi(x) / d theta = -y * phi(x)
                    # parameter := parameter - alpha * gradient
                    parameter_gradient = -yy * self.phi(x)
                    self.theta = self.theta - parameter_gradient
                    theta_updated = True
