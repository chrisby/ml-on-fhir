class FHIRBaseObject():

    def __init__(self, resource_dict: dict, fhir_resources: list, fhir_client: object=None):
        self._dict = resource_dict
        self.fhir_client = fhir_client

        for resource in fhir_resources:
            if resource in resource_dict.keys():
                setattr(self, resource, resource_dict[resource])
