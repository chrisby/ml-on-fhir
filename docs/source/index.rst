Welcome to ML on FHIR's documentation!
======================================
.. highlight:: python
   :linenothreshold: 1



Installation
^^^^^^^^^^^^
TODO

Getting Started
^^^^^^^^^^^^^^^

Connecting to a FHIR Server
---------------------------
To connect to a FHIR server, create a ``FHIRClient`` object and provide its ``BaseURL``:: 

   from fhir_client import FHIRClient
   client = FHIRClient(service_base_url='https://r3.smarthealthit.org')

The server's compatibility statement is queried to determine whether the connection was sucessful established.

Get an Overview of your Data
------------------------------

Before querying patients that belong to a specific cohort, we can get an overview of available **procedures** and via::

   import pandas as pd
   procedures = client.get_all_procedures()
   pd.DataFrame([prod.code['coding'][0] for prod in procedures]).drop_duplicates().sort_values(by=['display']).head()

This might take a while but will give you an overview of available procedures. E.g.

=====  ===========  ==========================================  =========
ID     code         display                                     system
=====  ===========  ==========================================  =========
893    183450002    Admission to burn unit                      http://snomed.info/sct
83     305428000    Admission to orthopedic department          http://snomed.info/sct
13687  35637008     Alcohol rehabilitation                      http://snomed.info/sct
=====  ===========  ==========================================  =========

Similarily, we can receive a list of available **conditions** via::

   conditions = client.get_all_conditions()
   pd.DataFrame([cond.code['coding'][0] for cond in conditions]).drop_duplicates(subset=['display']).sort_values(by='display', ascending=True).head()
   
=====  ===========  ==========================================  =========
ID     code         display                                     system
=====  ===========  ==========================================  =========
488    30473006     Abdominal pain                              http://snomed.info/sct
140    102594003    Abnormal ECG                                http://snomed.info/sct
6801   26079004     Abnormal involuntary movement               http://snomed.info/sct
=====  ===========  ==========================================  =========
   
Query Patients
--------------

With a list of available conditions we can query patients for which a certain condition was diagnosed. To do so we can either use the code of a coding nomenclature (e.g. *SNOMED*) or its readable name::

   patients_by_condition_text = client.get_patients_by_condition_text("Abdominal pain")
   patients_by_procedure_code = client.get_patients_by_procedure_code("http://snomed.info/sct","73761001")

Machine Learning
----------------
TODO


.. toctree::
   :maxdepth: 2
   :caption: Customize MLonFHIR

   customize/index
