class FHIRBaseObject():

    def __init__(self, resource_dict: dict, fhir_resources: list):
        self._dict = resource_dict

        for resource in fhir_resources:
            if resource in resource_dict.keys():
                setattr(self, resource, resource_dict[resource])
