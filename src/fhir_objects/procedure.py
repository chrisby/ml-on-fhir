from .fhir_resources import procedure_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Procedure(FHIRBaseObject):

    def __init__(self, resource_dict: dict):
        if resource_dict['resourceType'] != 'Patient':
            raise ValueError("Can not generate a Procedure from {}".format(resource_dict['resourceType']))

        super().__init__(resource_dict, procedure_resources)

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Procedure has no name attribute."
