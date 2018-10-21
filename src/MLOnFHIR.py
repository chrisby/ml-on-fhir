from typing import Union, List
from Patient import Patient
from Preprocessing import Preprocessing

from sklearn.neighbors import KNeighborsClassifier

from typing import List

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
