from .fhir_resources import observation_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Observation(FHIRBaseObject):

    def __init__(self, resource_dict: dict):
        super().__init__(resource_dict, observation_resources)

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Observation has no name attribute."
