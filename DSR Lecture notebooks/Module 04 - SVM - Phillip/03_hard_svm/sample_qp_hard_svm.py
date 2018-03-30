import numpy
import cvxopt


class QPHardSVM(object):
    def __init__(self):
        self.theta = None

    def fit(self, X, y):
        """
        Learns parameter vector self.theta from data X and binary labels y.

        y should have -1 for negative class and +1 for positive.
        X will be augmented with an intercept term in case self.fit_intercept is True.

        ---

        Solves a quadratic program

            minimize    (1/2)*x'*P*x + q'*x
            subject to  G*x <= h
                        A*x = b.
        Input arguments.

            P is a n x n dense or sparse 'd' matrix with the lower triangular
            part of P stored in the lower triangle.  Must be positive
            semidefinite.
            q is an n x 1 dense 'd' matrix.
            G is an m x n dense or sparse 'd' matrix.
            h is an m x 1 dense 'd' matrix.
            A is a p x n dense or sparse 'd' matrix.
            b is a p x 1 dense 'd' matrix or None.
        """
        assert X.shape[0] == y.shape[0]
        intercept = numpy.ones((X.shape[0], 1))
        X = numpy.concatenate((X, intercept), axis=1)

        # m rows, n columns
        m, n = X.shape[0], X.shape[1]

        P = numpy.eye(X.shape[1])
        q = numpy.zeros((X.shape[1], 1))
        G = -y.reshape(-1,1)*X
        h = -numpy.ones((X.shape[0], 1))

        print(P.shape, q.shape, G.shape, h.shape)

        sol = cvxopt.solvers.qp(
            # n x n
            P=cvxopt.matrix(P),
            # n x 1
            q=cvxopt.matrix(q),
            # data constraints
            # m x n (nSamples x nFeatures) = -yX
            G=cvxopt.matrix(G),
            h=cvxopt.matrix(h)
        )
        self.theta = sol['x']
