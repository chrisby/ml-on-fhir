class FHIRBaseObject():
    """
    Base class that implements FHIR resources.

    Attributes:
         All FHIR attributes specified in the respective resource variable in fhir_resources.py
    """
    def __init__(self, resource_dict: dict, fhir_resources: list, fhir_client: object=None):
        self.fhir_client = fhir_client

        for resource in fhir_resources:
            if resource in resource_dict.keys():
                setattr(self, resource, resource_dict[resource])
