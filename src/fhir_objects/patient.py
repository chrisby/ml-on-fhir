from .fhir_resources import patient_resources, date_format
from .fhir_base_object import FHIRBaseObject

import datetime as dt
import logging


class Patient(FHIRBaseObject):
    """
    Class that implements FHIR's patient resource.

    Attributes:
         All FHIR attributes specified in patient_resources 
    """

    def __init__(self, **kwargs):
        resource_dict = kwargs['resource_dict']
        if resource_dict['resourceType'] != 'Patient':
            raise ValueError("Can not generate a Patient from {}".format(
                resource_dict['resourceType']))

        kwargs['fhir_resources'] = patient_resources
        super().__init__(**kwargs)

        # Retrieve all observations for the patient
        self.observations = self.fhir_client.get_observation_by_patient(
            self.id)

        self._process_observations()

    def _process_observations(self):
        """
        Sets observations as patient attributes
        """
        for preprocessor in self.fhir_client.observation_preprocessors:
            attribute, value = preprocessor().fit(
                self.observations).transform(self.observations)
            setattr(self, attribute, value)

    def __str__(self):
        if hasattr(self, 'name'):
            name_list = self._dict['name']
            return str(name_list)
        else:
            return "Patient has no name attribute."
