Welcome to ML on FHIR's documentation!
======================================

Here is some text::

    print('test')

Installation
^^^^^^^^^^^^
TODO

Getting Started
^^^^^^^^^^^^^^^

To connect to a FHIR server create a FHIRClient object and provide its BaseULR

.. codeblock:: python
    :linenos:

    from fhir_client import FHIRClient
    client = FHIRClient(service_base_url='https://r3.smarthealthit.org', logger=logger)


.. toctree::
   :maxdepth: 2
