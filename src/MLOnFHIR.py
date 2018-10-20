from typing import Union, List
from Patient import Patient
from Preprocessing import Preprocessing

class Clustering():

	def __init__(self, fhir_class: Union[Patient]):
		self.preprocessor = Preprocessing(fhir_class)


	def cluster_on(self, X: List[Union[Patient]], attr: str, how: str='kmeans'):
		try:
			X_preprocessed = self.preprocessor.preprocess_on(X, attr)
			return X_preprocessed
		except:
			raise
