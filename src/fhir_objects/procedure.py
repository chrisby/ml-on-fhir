from .fhir_resources import procedure_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Procedure(FHIRBaseObject):
    """
    Class that implements FHIR's procedure resource.

    Attributes:
         All FHIR attributes specified in patient_resources 
    """

    def __init__(self, **kwargs):
        resource_dict = kwargs['resource_dict']
        if resource_dict['resourceType'] != 'Procedure':
            raise ValueError("Can not generate a Procedure from {}".format(
                resource_dict['resourceType']))

        kwargs['fhir_resources'] = procedure_resources
        super().__init__(**kwargs)
