Welcome to ML on FHIR's documentation!
======================================
.. highlight:: python
   :linenothreshold: 1

.. toctree::
   :maxdepth: 2
   
Installation
^^^^^^^^^^^^
TODO

Getting Started
^^^^^^^^^^^^^^^

Connecting to a FHIR Server
---------------------------
To connect to a FHIR server, create a ``FHIRClient`` object and provide its ``BaseURL``:: 

   from fhir_client import FHIRClient
   client = FHIRClient(service_base_url='https://r3.smarthealthit.org', logger=logger)

The server's compatibility statement is queried to determine whether the connection was sucessful established.

Query Patients
--------------

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
   
