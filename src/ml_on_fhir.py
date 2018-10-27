import sys
from typing import List, Union
from importlib import import_module
import logging

from Patient import Patient

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer
from sklearn.utils.validation import column_or_1d


class MLOnFHIR(BaseEstimator, ClassifierMixin):
    """
    """

    def __init__(self, fhir_class: Union[Patient], feature_attrs: List[str], label_attrs: List[str]):
        self.fhir_class = fhir_class
        self.label_attrs = label_attrs
        self.feature_attrs = feature_attrs
        # Import transformers for preprocessing of fhir features
        self.transformers = (feature_attrs, label_attrs)

    @property
    def feature_attrs(self):
        """list: List of fhir attributes that will be used as features"""
        return self._feature_attrs

    @feature_attrs.setter
    def feature_attrs(self, value: List[str]):
        self._feature_attrs = value

    @feature_attrs.deleter
    def feature_attrs(self):
        del self._feature_attrs

    @property
    def label_attrs(self):
        """list: List of fhir attributes that will be used as labels. Currently no multi labels allowes"""
        return self._label_attrs

    @label_attrs.setter
    def label_attrs(self, value: List[str]):
        if len(value) > 1:
            raise ValueError(
                "Only one label attribute is allowed. You chose {}".format(len(value)))
        else:
            self._label_attrs = value

    @label_attrs.deleter
    def label_attrs(self):
        del self._label_attrs

    @property
    def fhir_class(self):
        """type: The class name for which an ML helper should be generated"""
        return self._fhir_class

    @fhir_class.setter
    def fhir_class(self, value: Union[Patient]):
        # TODO Check whether KNOWN class has been passed
        if type(value) != type:
            raise ValueError("""{} is not a type but a {}.
				Please use the desired class you want to process (e.g. Patient)""".format(value, type(value)))
        else:
            self._fhir_class = value

    @fhir_class.deleter
    def fhir_class(self):
        del self._fhir_class

    @property
    def transformers(self):
        """dict: Dictionary with fhir_attr as key and its respective preprocessor class as value"""
        return self._transformers

    @transformers.setter
    def transformers(self, attrs: tuple):
        self._transformers = dict()
        preprocessing_module = import_module("preprocessing")
        for fhir_attr in attrs[0] + attrs[1]:
            class_name = self._get_preprocessing_classname(
                self._fhir_class.__module__, fhir_attr)
            try:
                self._transformers[fhir_attr] = getattr(
                    preprocessing_module, class_name)()
            except AttributeError:
                raise AttributeError("""Module 'preprocessing' has no attribute {}. 
                	Feel free to implement your custom class in module 'preprocessing' with signature {}(BaseEstimator).
""".format(class_name, class_name))

    @transformers.deleter
    def transformers(self):
        del self._transformers

    def _get_preprocessing_classname(self, fhir_class: str, fhir_attr: str):
        """
        Generates a string for the import of respective preprocessing class

        Args:
                fhir_class (str):	The module name of respective fhir_class (e.g. Patient)
                fhir_attr (str): 	The fhir attribute for which we want to import the preprocessing class (e.g. age)
        """
        return ''.join([fhir_class.capitalize(), fhir_attr.capitalize(), "Processor"])

    def transform(self, X, **transform_params):
        pass

    def fit(self, data: List[Union[Patient]], sklearn_clf: BaseEstimator, **fit_params):
        """
        Method that generates and executes the preprocessing and training pipeline.
        For each fhir attribute its respective preprocesser will be used

            Args:
                data (list): 	A list of fhir objects (e.g. Patient)
                sklearn_clf (BaseEstimator): A sklearn classifier object
        """

        # Get list of patients and their fhir attrs represented as list
        logging.info("Extracting attributes from data set")
        data_matrix = [[getattr(fhir_obj, fhir_attr)
                        for fhir_attr in self.feature_attrs + self.label_attrs] for fhir_obj in data]

        # Generate feature and label preprocessing pipeline
        pipeline = []
        for idx, fhir_attr in enumerate(self.feature_attrs + self.label_attrs):
            step_name = "{}_{}".format(idx, fhir_attr)
            step_class = self.transformers[fhir_attr]
            pipeline.append((step_name, step_class, [idx]))

        ct = ColumnTransformer(pipeline)

        logging.info("Preprocessing data")
        # Caution: The pipeline returns preprocessed features AND label
        complete_data_matrix = ct.fit_transform(data_matrix)
        X = complete_data_matrix[:, :len(self.feature_attrs)]
        y = complete_data_matrix[:, len(self.feature_attrs):]

        logging.info("Started training of clf")
        self.clf = sklearn_clf()
        self.clf.fit(X, column_or_1d(y))
        logging.info("Training completed")

        return X, y, self.clf

    def predict(self, X):
        return self.clf.predict(X)

    def score(self, X, y=None):
        return self.clf.score(X, y)


class Classifier():

    def __init__(self, fhir_class: Union[Patient]):
        self.preprocessor = Preprocessing(fhir_class)

    def classify_on(self, X: List[Union[Patient]], feature_attrs: List[str], label_attrs: List[str], how: str='knn'):
        try:
            X_preprocessed = self.preprocessor.preprocess_on(X, feature_attrs)
            y = self.preprocessor.preprocess_on(X, label_attrs)

            return X_preprocessed, y
        except:
            raise
