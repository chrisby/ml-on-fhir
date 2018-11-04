from .fhir_resources import observation_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Observation(FHIRBaseObject):

    def __init__(self, resource_dict: dict):
        if resource_dict['resourceType'] != 'Observation':
            raise ValueError("Can not generate an Observation from {}".format(
                resource_dict['resourceType']))

        super().__init__(resource_dict, observation_resources)

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Observation has no name attribute."
