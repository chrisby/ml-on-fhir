ObservationProcessors
^^^^^^^^^^^^^^^^^^^^^
.. highlight:: python
   :linenothreshold: 1

To use patient features in a machine learning task, we will extract them from the FHIR `Observation Resource 
<https://www.hl7.org/fhir/observation.html#resource>`_. Depending on how your server is set up, the way we can extract desired observation values might differ. In the following example we will use `LOINC codes
<https://loinc.org/>`_ to extract the latest **BMI measurement** of a patient.::

	from ml_on_fhir.preprocessing import AbstractObservationProcessor, get_coding_condition

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


.. note:: The name of your ``OberservationProcessor`` should always follow the following naming scheme: ``Observation<CustomIdentifier>``. 

In line 9, we define the name of the feature and how we will reference 

::

	from ml_on_fhir.fhir_client import FHIRClient
	client = FHIRClient(service_base_url='https://r3.smarthealthit.org')

	client.preprocessor.register_preprocessor(ObservationLatestBmiProcessor)

	ml_fhir = MLOnFHIRClassifier(Patient, feature_attrs=['bmiLatest'], label_attrs=['gender'], preprocessor=preprocessor)

Note that some patient attributes like ``gender`` are already provided through a similar mechanism with ``PatientProcessors``. Read more about them `here
<https://ml-on-fhir.readthedocs.io/en/latest/customize/PatientProcessor.html>`_.

