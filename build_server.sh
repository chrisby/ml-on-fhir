docker build -t smartonfhir/hapi:r3-synthea --build-arg FHIR=dstu3 --build-arg DATA=./databases/r3/synthea --build-arg CLI_OPTS=-Xmx1024m --squash .
