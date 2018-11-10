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

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Condition has no name attribute."
