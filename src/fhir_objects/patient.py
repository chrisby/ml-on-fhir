from .fhir_resources import patient_resources, date_format
from .fhir_base_object import FHIRBaseObject

import datetime as dt


class Patient(FHIRBaseObject):

    def __init__(self, **kwargs):
        resource_dict = kwargs['resource_dict']
        if resource_dict['resourceType'] != 'Patient':
            raise ValueError("Can not generate a Patient from {}".format(
                resource_dict['resourceType']))

        kwargs['fhir_resources'] = patient_resources
        super().__init__(**kwargs)

        print(self.fhir_client)

        # Retrieve all Observations for the patient
        #self.observations = get_observation_by_patient

    def __str__(self):
        if self.name:
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Patient has no name attribute."
