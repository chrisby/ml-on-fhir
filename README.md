# ml-on-fhir

## Install the hapi FHIR command line interface
Use the `hapi-fhir-cli` to deploy an empty FHIR server locally. Install the command line tool via the instructions on the [project page](http://hapifhir.io/doc_cli.html) or for Mac users:
```
$ brew install hapi-fhir-cli
```
After installation try
```
$ hapi-fhir-cli
```
to see if the command line tool was properly installed. 

## Start the server
The patients we will later generate will be compatible with `FHIR` version `R4`. To start the FHIR server on port 8080 run:
```
$ hapi-fhir-cli run-server -p 8080 -v r4
```
## Generate Patients
This repository makes use of the [Synthea<sup>TM</sup> Patient Generator](https://github.com/synthetichealth/synthea).
To check if the tests run (Java 1.8 or above is required) do the following (in a new terminal):
```
$ cd synthea
$ ./gradlew build check test
```
To generate `100` patients you simply need to run the following command. The patients will then be created in `../data/synthea/fhir_r4`.
```
$ ./run_synthea -s 42 -p 100
```
## Import Patients into database
Once all patients are generated, the last step is to import them into our database. Simply run:
```
$ ./import_data.sh
```
