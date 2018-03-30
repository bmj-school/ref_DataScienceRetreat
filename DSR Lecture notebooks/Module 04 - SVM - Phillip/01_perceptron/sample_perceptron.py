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

        self.theta = np.random.randn(X.shape[1], 1)
        theta_updated = True
        while theta_updated:
            theta_updated = False
            for i in range(X.shape[0]):
                x, yy = X[i, :], y[i]
                # if label yy and sign of decision function do not agree
                # sample x on wrong side of the hyperplane
                if yy * (np.dot(self.theta.T, x.reshape(-1, 1))) <= 0:
                    # -y * theta.T * x / d theta = -y*x
                    # parameter := parameter - alpha * gradient
                    parameter_gradient = -yy * x.reshape(-1, 1)
                    self.theta = self.theta - parameter_gradient
                    theta_updated = True
