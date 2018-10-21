import numpy as np

from Patient import Patient
from typing import Union, List

class Preprocessing():

	def __init__(self, fhir_class: Union[Patient]):
		if type(fhir_class) != type:
			raise ValueError("""{} is not a type but a {}. 
				Please use the desired class you want to process (e.g. Patient)""".format(fhir_class, type(fhir_class)))
		else:
			self.fhir_class = fhir_class

	def get_preprocessing_func(self, attr: str):
		needed_module_name = self.fhir_class.__module__.lower()
		needed_func_name = ('_'.join(['preprocess_{}'.format(needed_module_name), attr]))
		if needed_func_name not in dir(self):
			available_attributes = [x.split('_')[2] for x in dir(self) if needed_module_name in x ]
			if len(available_attributes) > 0:
				raise NotImplementedError("""Sorry, we don't know how to preprocess the attribute {}. 
					Available attributes are {}.""".format(attr, ', '.join(available_attributes)))
			else:
				raise NotImplementedError("Sorry, we don't know how to preprocess the attribute {}.".format(attr))
		else:
			return needed_func_name

	
	def preprocess_on(self, X: List[Union[Patient]], attrs: List[str]):
		preprocessed_data = np.empty(shape=(len(X), len(attrs)))
		preprocessing_funcs = [self.get_preprocessing_func(attr) for attr in attrs]
		for attr_index, preprocessing_func in enumerate(preprocessing_funcs):
			preprocessed_data[:,attr_index] = getattr(self, preprocessing_func)(X)
		return preprocessed_data


	def preprocess_patient_age(self, X: List[Patient]):
		return [x.age for x in X]

