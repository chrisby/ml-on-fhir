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

.. toctree::
   :maxdepth: 2
