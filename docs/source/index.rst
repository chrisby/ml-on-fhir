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
   client = FHIRClient(service_base_url='https://r3.smarthealthit.org', logger=logger)

The server's compatibility statement is queried to determine whether the connection was sucessful established.

Query Patients
--------------

Before querying patients that belong to a specific cohort, we can get an overview of available **procedures** and **conditions** via::

   import pandas as pd
   procedures = client.get_all_procedures()
   pd.DataFrame([prod.code['coding'][0] for prod in procedures]).drop_duplicates().sort_values(by=['display']).head()

This might take a while but will give you an overview of available procedures. E.g.:

=====  ========  =======  =========
ID     code      display  system
=====  ========  =======  =========
893	183450002	Admission to burn unit	http://snomed.info/sct
1911	305340004	Admission to long stay hospital	http://snomed.info/sct
83	305428000	Admission to orthopedic department	http://snomed.info/sct
6217	305433001	Admission to trauma surgery department	http://snomed.info/sct
13687	35637008	Alcohol rehabilitation	http://snomed.info/sct
=====  =====  =======

.. toctree::
   :maxdepth: 2
