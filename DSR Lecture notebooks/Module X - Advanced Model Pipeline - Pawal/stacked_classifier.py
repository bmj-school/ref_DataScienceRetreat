import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score

from cross_validation import cross_val_apply


class StackedClassifier(BaseEstimator, TransformerMixin):

    def __init__(self, estimators, mixer,
                 n_jobs=1, cv=5, probability=False):
        self.estimators = estimators
        self.mixer = mixer
        self.n_jobs = n_jobs
        self.cv = cv
        self.probability = probability

    def fit(self, X, y=None):
        X_ = self._prepare_data(X, y)
        self._fit_models(X, y)
        self.mixer.fit(X_, y)
        return self

    def _prepare_data(self, X, y, predict=False):
        tmp_predictions = []
        if predict is False:
            for estimator in self.estimators:
                tmp_predictions.append(
                    self._cross_val_predict_one_estimator(
                        X, y, estimator
                        )
                    )
        else:
            for estimator in self.estimators:
                tmp_predictions.append(
                    self._prediction_model(
                        X, y, estimator
                        )
                    )
        tmp_predictions = list(map(
            lambda v: v.reshape(len(X), -1),
            tmp_predictions
        ))
        tmp_predictions = np.hstack(tmp_predictions)
        return pd.DataFrame(data=tmp_predictions)

    def predict(self, X, y=None):
        X_ = self._prepare_data(X, y, True)
        return self.mixer.predict(X_)

    def predict_proba(self, X, y=None):
        X_ = self._prepare_data(X, y, True)
        return self.mixer.predict_proba(X_)

    def _prediction_model(self, X, y, estimator):
        if self.probability is True:
            pred_tmp = estimator.predict_proba(X)[:,1].reshape(-1,1)
        else:
            pred_tmp = estimator.predict(X)
        return pred_tmp

    def _cross_val_predict_one_estimator(self, X, y, estimator):
        function = 'predict'
        if self.probability is True:
            function = 'predict_proba'
        return cross_val_apply(
            estimator,
            X,
            y,
            self.cv,
            n_jobs=self.n_jobs,
            decision_func=function
        )[:,1].reshape(-1,1)

    def _fit_models(self, X, y):
        for estimator in self.estimators:
            estimator.fit(X, y)
        return self

    def score(self, X, y, sample_weight=None):
        y_pred = self.predict(X)
        return accuracy_score(y, y_pred)
