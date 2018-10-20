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
			if len(name_list) >= 1:
				name_obj = name_list[0]

				# If text attribute is available use this as string
				if 'text' in name_obj.keys():
					return name_obj['text']
				else:
					# Determine whether name object has a specific use
					if 'use' in name_obj.keys():
						if name_obj['use'] == 'official':
							prefixes = ''
							if 'prefix' in name_obj.keys():
								prefixes = ' '.join(name_obj['prefix'])

							family_name = name_obj['family']

							given_names = ''
							if 'given' in name_obj.keys():
								given_names = ' '.join(name_obj['given'])

							return "{} {}, {}".format(prefixes, family_name, given_names)

			else:
				return "Patient has no name attribute."


		else:
			# Empty patient
			return "Empty Patient"