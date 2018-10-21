from FHIRResources import patient_resources, date_format

import datetime as dt

class Patient:

	def __init__(self, resource_dict: dict):
		self._dict = resource_dict

		for resource in patient_resources:
			if resource in resource_dict.keys():
				setattr(self, resource, resource_dict[resource])

		if hasattr(self, 'birthDate'):
			self.age = self.birthDate

	@property
	def age(self):
		return self._age

	@age.setter
	def age(self, birthdate: str):
		b_date = dt.datetime.strptime(birthdate, date_format)
		self._age = int((dt.datetime.now().date() - b_date.date()).days/365)



	def __str__(self):
		if self.name:
			name_list = self._dict['name']
			return name_list
		else:
			return "Patient has no name attribute."