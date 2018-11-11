import sys
from typing import List, Union, Callable
from importlib import import_module
import logging

from fhir_objects.patient import Patient

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer
from sklearn.utils.validation import column_or_1d
from sklearn.utils.multiclass import type_of_target
import sklearn.metrics as m


class MLOnFHIR(BaseEstimator, ClassifierMixin):
    """
    Core class that acts as a classifier and preprocessing entity.
    It creates the preprocessing pipeline based on fhir attributes and their preprocessing transformers. 

    Args:
        fhir_class (Union[Patient]): A class from the fhir_objects module (e.g. Patient)
        feature_attrs (List[str]): A list of fhir attributes from respective fhir_class
        label_attrs (List[str]): A list of (as of now) one fhir attribute from respective fhir_class to be used as label

    Attributes:
        transformers (dict): Dictionary that maps a fhir attribute to its respective transformer class 
                             (e.g preprocessing.PatientBirthdateProcessor)
    """

    def __init__(self, fhir_class: Union[Patient], feature_attrs: List[str], label_attrs: List[str]):
        self.fhir_class = fhir_class
        self.label_attrs = label_attrs
        self.feature_attrs = feature_attrs
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
        """list: List of fhir attributes that will be used as labels. Currently no multi labels allows"""
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
                self._fhir_class.__name__, fhir_attr)
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

    def transform(self, X, **transform_params):
        pass

    def fit(self, data: List[Union[Patient]], sklearn_clf: BaseEstimator, **fit_params):
        """
        Generates and executes the preprocessing and training pipeline.
        For each fhir attribute its respective preprocessor will be used

        Args:
            data (list): 	A list of fhir objects (e.g. Patient)
            sklearn_clf (BaseEstimator): Instance of a sklearn classifier

        Returns:
            (list, list, object): A tuple of complete data matrix, labels and trained clf
        """

        # Get list of patients and their fhir attrs represented as list
        logging.info("Extracting attributes from data set")
        data_matrix = self._get_data_matrix(data)

        # Generate feature and label preprocessing pipeline
        pipeline = self._generate_pipeline()
        ct = ColumnTransformer(pipeline)

        logging.info("Preprocessing data")
        # Caution: The pipeline returns preprocessed features AND label
        complete_data_matrix = ct.fit_transform(data_matrix)
        X = complete_data_matrix[:, :len(self.feature_attrs)]
        y = complete_data_matrix[:, len(self.feature_attrs):]
        y = column_or_1d(y)

        # Check y suitability for classification
        if type_of_target(y) in ["continuous", "continuous-multioutput", "unknown"]:
            logging.warning("The target label is not suitable for classification (type: {})".format(
                type_of_target(y)))

        logging.info("Started training of clf")
        self.clf = sklearn_clf
        self.clf.fit(X, column_or_1d(y))
        logging.info("Training completed")

        return X, y, self.clf

    def predict(self, X):
        return self.clf.predict(X)

    def score(self, X, y):
        return self.clf.score(X, y)

    def evaluate(self, X, y, print_report=False):
        """
        Depending on the classification task, evaluate the predictor and 
        store its performance.

        Different use-cases:
        * Binary: after checking class imbalance on the target values, 
          computes the accuracy, precision, recall, AUROC, AUPRC, balanced 
          accuracy, F1-score, confusion matrix (tp, fp, fn, tn)

        * Multiclass: computes the accuracy, F1-score, confusion matrix and 
          precision/recall information for each class

        * Multilabel: computes the accuracy, AUROC, F1-score, average precision
          score, precision/recall information for each class

        All cases can print the classification report if print_report is 
        set to true

        Args:
            X (array-like):     Test samples
            y (array-like):     True label of the test samples

        Returns:
            None
        """
        # Start by predicting values
        y_pred = self.predict(X)
        y_type = self._get_classification_type(y, y_pred)

        # No metrics support multiclass-multioutput:
        if y_type == "multiclass-multioutput":
            logging.warning("No metrics support multiclass-multioutput target")
            return

        # Result dict
        eval_dict = dict()
        # Start by shared evaluations: accuracy, F1-score
        eval_dict["accuracy"] = m.accuracy_score(y, y_pred)
        eval_dict["f1_score"] = m.f1_score(y, y_pred, average="micro")
        # values for each class
        eval_dict["precision"], eval_dict["recall"], eval_dict["f1_score_class"], \
            eval_dict["support"] = m.precision_recall_fscore_support(
                y, y_pred, average=None)

        # Binary case
        if y_type == "binary":
            # Check class imbalance, custom def: 20%
            support = eval_dict["support"]
            if 4 * support[0] <= support[1] or support[0] >= 4 * support[1]:
                logging.warning(
                    "Classes are imbalanced, some evaluation metrics have to be considered carefully.")
                eval_dict["balanced_accuracy"] = m.balanced_accuracy_score(
                    y_true, y_pred)
            # TODO Check if y_pred scores are probabilistic
            eval_dict["AUROC"] = m.roc_auc_score(y, y_pred)
            precision, recall, _ = m.precision_recall_curve(y, y_pred)
            eval_dict["AUPRC"] = m.auc(recall, precision)
            # Confusion matrix
            eval_dict["tn"], eval_dict["fp"], eval_dict["fn"], \
                eval_dict["tp"] = m.confusion_matrix(y, y_pred).ravel()

        elif y_type == "multiclass":
            # Confusion matrix
            eval_dict["confusion_matrix"] = m.confusion_matrix(y, y_pred)

        elif y_type == "multilabel-indicator":
            # AUROC
            eval_dict["AUROC"] = m.roc_auc_score(y, y_pred, average="micro")
            eval_dict["average_precision"] = m.average_precision_score(
                y, y_pred, average="micro")

        if print_report:
            print(m.classification_report(y, y_pred))

        return eval_dict

    def _get_preprocessing_classname(self, class_name: str, fhir_attr: str):
        """
        Generates a string for the import of respective preprocessing class

        Args:
            class_name (str):	The class name of respective fhir_class (e.g. Patient)
            fhir_attr (str): 	The fhir attribute for which we want to import the preprocessing class (e.g. age)

        Returns:
            str: Respective class name 
        """
        return ''.join([class_name.capitalize(), fhir_attr.capitalize(), "Processor"])

    def _get_data_matrix(self, data: List[Union[Patient]]):
        """
        Transform the list of fhir objects into a list of their attributes

        Args:
            data (list): 	A list of fhir objects (e.g. Patient)

        Returns:
            list: A list of fhir attribute dictionaries for fhir object of the input
        """
        return [[getattr(fhir_obj, fhir_attr)
                 for fhir_attr in self.feature_attrs + self.label_attrs] for fhir_obj in data]

    def _generate_pipeline(self):
        """
        Generates a list of tuples of the form (name, preprocessor_class, [col_index])

        Returns:
            list: A list to be used in sklearn.compose.ColumnTransformer
        """
        pipeline = []
        for idx, fhir_attr in enumerate(self.feature_attrs + self.label_attrs):
            step_name = "{}_{}".format(idx, fhir_attr)
            step_class = self.transformers[fhir_attr]
            pipeline.append((step_name, step_class, [idx]))
        return pipeline

    def _get_classification_type(self, y, y_pred):
        # Get predicted types (see sklearn.utils.type_of_target)
        type_pred = type_of_target(y_pred)
        type_true = type_of_target(y)
        y_type = set([type_true, type_pred])

        if y_type == set(["binary", "multiclass"]):
            y_type = set(["multiclass"])

        if len(y_type) > 1:
            logging.info("Classification can't handle a mix of {} and {} targets."
                         .format(y_type[0], y_type[1]))
        # Take first value of set
        return y_type.pop()
