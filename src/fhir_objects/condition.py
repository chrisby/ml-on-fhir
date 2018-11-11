from .fhir_resources import condition_resources
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Condition(FHIRBaseObject):

    def __init__(self, **kwargs):
        resource_dict = kwargs['resource_dict']
        if resource_dict['resourceType'] != 'Condition':
            raise ValueError("Can not generate a Condition from {}".format(
                resource_dict['resourceType']))

        kwargs['fhir_resources'] = condition_resources
        super().__init__(**kwargs)
