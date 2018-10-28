from inspect import signature
import datetime as dt
import numpy as np
from typing import Union, List

from fhir_objects.Patient import Patient
from fhir_resources import date_format

from sklearn.base import BaseEstimator
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import column_or_1d


class FHIRLabelEncoder(BaseEstimator):
    """
    This is a simple wrapper of sklearn's LabelEncoder as at the time of
    development it was not compatible with sklearn.compose.ColumnTransfer
    """

    @classmethod
    def _get_param_names(self):
        return super()._get_param_names()

    def set_params(self, **params):
        return super().set_params(**params)

    def get_params(self, deep=True):
        return super().get_params(deep=deep)

    def transform(self, X, **transform_params):
        return self.y

    def fit(self, X, y=None, **fit_params):
        le = LabelEncoder()
        self.y = le.fit_transform(column_or_1d(X)).reshape(-1, 1)
        return self


class PatientBirthdateProcessor(BaseEstimator):
    """
    Calculates the age to use birthdate as a feature 
    """
    @classmethod
    def _get_param_names(self):
        return super()._get_param_names()

    def set_params(self, **params):
        return super().set_params(**params)

    def get_params(self, deep=True):
        return super().get_params(deep=deep)

    def transform(self, X, **transform_params):
        ages = []
        for birthdate in X:
            b_date = dt.datetime.strptime(birthdate[0], date_format)
            ages.append([int(
                            (dt.datetime.now().date() - b_date.date()).days / 365)])
        return np.array(ages)

    def fit(self, X, y=None, **fit_params):
        return self


class PatientGenderProcessor(FHIRLabelEncoder):
    """
    Encodes gender gender into integer values
    """
    @classmethod
    def _get_param_names(self):
        return super()._get_param_names()

    def set_params(self, **params):
        return super().set_params(**params)

    def get_params(self, deep=True):
        return super().get_params(deep=deep)

    def transform(self, X, **transform_params):
        return super().transform(X, **transform_params)

    def fit(self, X, y=None, **fit_params):
        return super().fit(X, y, **fit_params)
