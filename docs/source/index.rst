Welcome to ML on FHIR's documentation!
======================================
.. highlight:: python
   :linenothreshold: 1

Installation
^^^^^^^^^^^^
TODO

Getting Started
^^^^^^^^^^^^^^^

To connect to a FHIR server create a FHIRClient object and provide its BaseULR:: 

    from fhir_client import FHIRClient
    client = FHIRClient(service_base_url='https://r3.smarthealthit.org', logger=logger)


.. toctree::
   :maxdepth: 2
