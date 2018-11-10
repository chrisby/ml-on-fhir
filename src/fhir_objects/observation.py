from .fhir_resources import observation_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Observation(FHIRBaseObject):

    def __init__(self, **kwargs):
        resource_dict = kwargs['resource_dict']
        if resource_dict['resourceType'] != 'Observation':
            raise ValueError("Can not generate an Observation from {}".format(
                resource_dict['resourceType']))

        kwargs['fhir_resources'] = observation_resources
        super().__init__(**kwargs)

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Observation has no name attribute."
