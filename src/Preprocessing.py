from Patient import Patient
from typing import Union, List

class Preprocessing():

	def __init__(self, fhir_class: Union[Patient]):
		if type(fhir_class) != type:
			raise ValueError("{} is not a type but a {}. Please use the desired class you want to process (e.g. Patient)".format(fhir_class, type(fhir_class)))


		### This is currently an ugly way of storing which classes and attibutes can be preprocessed
		self.preprocessing_dict = { Patient: { 'address': self.preprocess_address } }

		if fhir_class not in self.preprocessing_dict.keys():
			raise NotImplementedError("Sorry, we don't know how to preprocess objects of type {}.".format(fhir_class))
		else:
			self.fhir_class = fhir_class
			self.class_preprocessing_functions = self.preprocessing_dict[fhir_class]

	def can_preprocess(self, attr: str):
		if attr not in self.class_preprocessing_functions:
			raise NotImplementedError("Sorry, we don't know how to preprocess the attribute {} of {}.".format(attr, self.fhir_class))
		else:
			return True

	
	def preprocess_address(self, X: List[Union[Patient]]):
		return ['test']


	def preprocess_on(self, X: List[Union[Patient]], attr: str):
		if self.can_preprocess(attr):
			return self.preprocessing_dict[self.fhir_class][attr](X)
			pass