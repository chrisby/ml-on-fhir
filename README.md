# ml-on-fhir

## Install the hapi fhir command line interface
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
