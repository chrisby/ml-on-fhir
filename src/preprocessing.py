from inspect import signature
import datetime as dt
from typing import Union, List, Type
import logging
import numpy as np
import re
from importlib import import_module
import types


from fhir_objects.patient import Patient
from fhir_objects.fhir_resources import date_format

from sklearn.base import BaseEstimator
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import column_or_1d


def register_preprocessor(processor_class: BaseEstimator):
    """
    Registers a new preprocessing class with MLOnFhir.
    Preprocessors with the same class name will be overwritten

    Args:
        processor_class (BaseEstimator): Class that implements sklearn.base.BaseEstimator interface
    """
    preprocessing_module = import_module(
        get_observation_preprocessors.__module__)
    preprocessing_class_name = processor_class.__name__
    if hasattr(preprocessing_module, preprocessing_class_name):
        logging.warning("Preprocessor {} already exists. Will be overridden.".format(
            preprocessing_class_name))

    setattr(preprocessing_module, preprocessing_class_name, processor_class)

    # If a non-patient processor has been registered, we need to add one.
    if preprocessing_class_name[:len("Patient")] != "Patient":
        logging.info("Adding Patient Processor for {}".format(
            preprocessing_class_name))
        tmp_obj = processor_class()
        if not hasattr(tmp_obj, 'patient_attribute_name'):
            del tmp_obj
            raise ValueError(
                "Class {} does not have a patient_attribute_name attribute. Will not generate Patient Processor")
        else:
            new_name = 'Patient{}Processor'.format(
                tmp_obj.patient_attribute_name)
            logging.info(
                "Name of patient processor will be {}".format(new_name))
            new_class = PatientProcessorFactory(new_name)
            register_preprocessor(new_class)


def get_observation_preprocessors():
    """
    Returns a list of registered observation processors.

    Returns:
        list: List of classes with the r'Observation[\w]+Processor' signature 
    """
    preprocessing_module = import_module(
        get_observation_preprocessors.__module__)
    preprocessors = []
    for member_name, member in preprocessing_module.__dict__.items():
        if callable(member):
            re_match = re.fullmatch(
                r'Observation[\w]+Processor', member_name)
            if re_match:
                preprocessors.append(member)
    if len(preprocessors) == 0:
        logging.warning(
            "Could not find any Observation preprocessors. Usage might be limited.")
    return preprocessors


def get_coding_condition(code_dict_list: list):
    """
    Defines a function that returns true if the coding of a given observation 
    fits one of the dicts in code_dict_list

    Args:
        code_dict_list (list): A list of dicts that define the code we are looking for

    Returns:
        func: A function that can be used in a filter expression of a list 
    """
    def conditions(observation):
        for code in observation.code['coding']:
            for code_dict in code_dict_list:
                if all (k in code.keys() for k in code_dict):
                    return all (code[k] == code_dict[k] for k in code_dict)
    return conditions

class PatientProcessorBaseClass(BaseEstimator):
    """
    Base class that is used for the generation of Patient Processors 
    """

    def transform(self, X, **transform_params):
        return X.astype(float)

    def fit(self, X, y=None, **fit_params):
        return self


def PatientProcessorFactory(class_name: str, base_class: Type[PatientProcessorBaseClass]=PatientProcessorBaseClass):
    """
    Helper class to generate Patient Processor classes with specific names

    Args:
        class_name (str): Name of the class to be generated
        base_class (class object): Base class 
    """
    new_cl = types.new_class(class_name, (base_class,))
    return new_cl


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


class PatientgenderProcessor(FHIRLabelEncoder):
    """
    Encodes gender gender into integer values
    """

    def transform(self, X, **transform_params):
        return super().transform(X, **transform_params)

    def fit(self, X, y=None, **fit_params):
        return super().fit(X, y, **fit_params)


class PatientbirthDateProcessor(BaseEstimator):
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

class ObservationLatestBmiProcessor(BaseEstimator):
    """
    Class to transform the FHIR observation resource with loinc code 39156-5 (BMI)
    to be usable as patient feature.
    """
    def __init__(self):
        self.patient_attribute_name = 'bmiLatest'
        
    def transform(self, X, **transform_params):
        conditions = get_coding_condition([{'system': 'http://loinc.org', 'code': '39156-5'}])
        bmis = list(filter(conditions, X))
        bmis = sorted(bmis, reverse=True)
        if len(bmis) >= 1:
            return self.patient_attribute_name, float(bmis[0].valueQuantity['value'])
        else:
            return self.patient_attribute_name, 0.0

    def fit(self, X, y=None, **fit_params):
        return self

class ObservationLatestWeightProcessor(BaseEstimator):
    """
    Class to transform the FHIR observation resource with loinc code 29463-7 (body weight)
    to be usable as patient feature.
    """
    def __init__(self):
        self.patient_attribute_name = 'weightLatest'
        
    def transform(self, X, **transform_params):
        conditions = get_coding_condition([{'system': 'http://loinc.org', 'code': '29463-7'}])
        weights = list(filter(conditions, X))
        weights = sorted(weights, reverse=True)
        if len(weights) >= 1:
            return self.patient_attribute_name, float(weights[0].valueQuantity['value'])
        else:
            return self.patient_attribute_name, 0.0

    def fit(self, X, y=None, **fit_params):
        return self

class ObservationLatestHeightProcessor(BaseEstimator):
    """
    Class to transform the FHIR observation resource with loinc code 8302-2 (body height)
    to be usable as patient feature.
    """
    def __init__(self):
        self.patient_attribute_name = 'heightLatest'
        
    def transform(self, X, **transform_params):
        condition = conditions = get_coding_condition([{'system': 'http://loinc.org', 'code': '8302-2'}])
        heights = list(filter(condition, X))
        heights = sorted(heights, reverse=True)
        if len(heights) >= 1:
            return self.patient_attribute_name, float(heights[0].valueQuantity['value'])
        else:
            return self.patient_attribute_name, 0.0

    def fit(self, X, y=None, **fit_params):
        return self