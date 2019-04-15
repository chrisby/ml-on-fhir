from .fhir_resources import observation_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Observation(FHIRBaseObject):
    """
    Class that implements FHIR's observation Resource.

    Attributes:
         All FHIR attributes specified in observation_resources 
    """

    def __init__(self, **kwargs):
        resource_dict = kwargs['resource_dict']
        if resource_dict['resourceType'] != 'Observation':
            raise ValueError("Can not generate an Observation from {}".format(
                resource_dict['resourceType']))

        kwargs['fhir_resources'] = observation_resources
        super().__init__(**kwargs)

    def __lt__(self, other):
        return (self.effectiveDateTime < other.effectiveDateTime)

    def __le__(self, other):
        return(self.effectiveDateTime <= other.effectiveDateTime)

    def __gt__(self, other):
        return(self.effectiveDateTime > other.effectiveDateTime)
