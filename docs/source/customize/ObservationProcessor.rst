ObservationProcessors
^^^^^^^^^^^^^^^^^^^^^


To use patient features in a machine learning task, we will extract them from the FHIR `Observation Resource 
<https://www.hl7.org/fhir/observation.html#resource>`_. Depending on how your server is set up, the way we can extract desired observation values might differ. In the following example we will use 'LOINC codes
<https://loinc.org/>'_ to extract the latest **BMI measurement** of a patient.::

    class ObservationLatestBmiProcessor(AbstractObservationProcessor):
        """
        Class to transform the FHIR observation resource with loinc code 39156-5 (BMI)
        to be usable as patient feature.
        """
        def __init__(self):
            super().__init__('bmiLatest')
            
        def transform(self, X, **transform_params):
            conditions = get_coding_condition([{'system': 'http://loinc.org', 'code': '39156-5'}])
            bmis = list(filter(conditions, X))
            bmis = sorted(bmis, reverse=True)
            if len(bmis) >= 1:
                return self.patient_attribute_name, float(bmis[0].valueQuantity['value'])
            else:
                return self.patient_attribute_name, 0.0

        def fit(self, X, y=None, **fit_params):
            return self

