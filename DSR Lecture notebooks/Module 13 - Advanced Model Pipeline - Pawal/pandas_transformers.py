import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline


class PandasSelector(BaseEstimator, TransformerMixin):

    def __init__(self, dtype=None, columns=None, inverse=False,
                 return_vector=True):
        self.dtype = dtype
        self.columns = columns
        self.inverse = inverse
        self.return_vector = return_vector

    def check_condition(self, x, col):
        cond = (self.dtype is not None and x[col].dtype == self.dtype) or \
               (self.columns is not None and col in self.columns)
        return self.inverse ^ cond

    def fit(self, x, y=None):
        return self

    def _check_if_all_columns_present(self, x):
        if not self.inverse and self.columns is not None:
            missing_columns = set(self.columns) - set(x.columns)
            if len(missing_columns) > 0:
                missing_columns_ = ','.join(col for col in missing_columns)
                raise KeyError('Keys are missing in the record: %s' %
                                   missing_columns_)

    def transform(self, x):
        # check if x is a pandas DataFrame
        if not isinstance(x, pd.DataFrame):
            raise KeyError('Input is not a pandas DataFrame')

        selected_cols = []
        for col in x.columns:
            if self.check_condition(x, col):
                selected_cols.append(col)

        # if the column was selected and inversed = False make sure the column
        # is in the DataFrame
        self._check_if_all_columns_present(x)

        # if only 1 column is returned return a vector instead of a dataframe
        if len(selected_cols) == 1 and self.return_vector:
            return x[selected_cols[0]]
        else:
            return x[selected_cols]


class PandasCategoricalExtractor(BaseEstimator, TransformerMixin):

    def __init__(self, columns=None, numerical_to_object=True):
        self.columns = columns
        self.numerical_to_object = numerical_to_object

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        if self.columns is None:
            self.columns = x.columns

        # convert all non object dtypes to unicode
        for col in x.columns:
            x[col] = x[col].map(unicode)

        return x.ix[:, self.columns].T.to_dict().values()


class MissingValuesFiller(BaseEstimator, TransformerMixin):

    def __init__(self, default=-1000):
        self.default = default

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x.fillna(self.default)


def make_pandas_categorical_vectorizer(columns):
    return make_pipeline(
        PandasCategoricalExtractor(columns=columns),
        DictVectorizer()
    )


class ApplyFunction(BaseEstimator, TransformerMixin):

    def __init__(self, columns, fun):
        self.columns = columns
        self.fun = fun

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        for col in self.columns:
            x[col] = x[col].map(self.fun)
        return x

