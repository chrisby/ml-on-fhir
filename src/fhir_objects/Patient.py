from fhir_resources import patient_resources, date_format

import datetime as dt


class Patient:

    def __init__(self, resource_dict: dict):
        self._dict = resource_dict

        for resource in patient_resources:
            if resource in resource_dict.keys():
                setattr(self, resource, resource_dict[resource])

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Patient has no name attribute."
