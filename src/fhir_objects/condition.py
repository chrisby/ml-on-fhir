from fhir_resources import condition_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Condition(FHIRBaseObject):

    def __init__(self, resource_dict: dict):
        super().__init__(resource_dict, condition_resources)

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Condition has no name attribute."
