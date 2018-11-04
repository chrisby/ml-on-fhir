from inspect import signature
import datetime as dt
from typing import Union, List
import logging
import numpy as np

from fhir_objects.patient import Patient
from fhir_objects.fhir_resources import date_format

from sklearn.base import BaseEstimator
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import column_or_1d

import inspect


def register_preprocessor(processor_class: BaseEstimator):
    """
    Registers a new preprocessing class with MLOnFhir.
    Preprocessors with the same class name will be overwritten

    Args:
        processor_class (BaseEstimator): Class that implements sklearn.base.BaseEstimator interface 
    """
    preprocessing_module = inspect.getmodule(register_preprocessor)
    preprocessing_class_name = processor_class.__name__
    if hasattr(preprocessing_module, preprocessing_class_name):
        logging.warning("Preprocessor {} already exists. Will be overridden.".format(
            preprocessing_class_name))

    setattr(preprocessing_module, preprocessing_class_name, processor_class)


class FHIRLabelEncoder(BaseEstimator):
    """
    This is a simple wrapper of sklearn's LabelEncoder as at the time of
    development it was not compatible with sklearn.compose.ColumnTransfer
    """

    def transform(self, X, **transform_params):
        return self.y

    def fit(self, X, y=None, **fit_params):
        le = LabelEncoder()
        self.y = le.fit_transform(column_or_1d(X)).reshape(-1, 1)
        return self


class PatientGenderProcessor(FHIRLabelEncoder):
    """
    Encodes gender gender into integer values
    """

    def transform(self, X, **transform_params):
        return super().transform(X, **transform_params)

    def fit(self, X, y=None, **fit_params):
        return super().fit(X, y, **fit_params)


class PatientBirthdateProcessor(BaseEstimator):
    """
    Calculates the age to use birthdate as a feature 
    """

    def transform(self, X, **transform_params):
        ages = []
        for birthdate in X:
            b_date = dt.datetime.strptime(birthdate[0], date_format)
            ages.append([int(
                            (dt.datetime.now().date() - b_date.date()).days / 365)])
        return np.array(ages)

    def fit(self, X, y=None, **fit_params):
        return self
