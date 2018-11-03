from .fhir_resources import patient_resources, date_format
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Patient(FHIRBaseObject):

    def __init__(self, resource_dict: dict):
        super().__init__(resource_dict, patient_resources)

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Patient has no name attribute."
