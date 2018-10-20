class Patient:

	def __init__(self, resource_dict: dict):
		self._dict = resource_dict

		if 'name' in resource_dict.keys():
			self.name = resource_dict['name']

		if 'address' in resource_dict.keys():
			self.address = resource_dict['address']

	def __str__(self):
		if self.name:
			name_list = self._dict['name']
			return name_list
		else:
			return "Patient has no name attribute."


		else:
			# Empty patient
			return "Empty Patient"