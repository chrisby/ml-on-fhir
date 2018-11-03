echo Importing Practitioner Information
curl http://localhost:8080/baseR --data-binary "@data/synthea/fhir_r4/practitionerInformation*.json" -H "Content-Type: application/fhir+json" 

echo Importing Hospital Information
curl http://localhost:8080/baseR --data-binary "@data/synthea/fhir_r4/hospitalInformation*.json" -H "Content-Type: application/fhir+json" 

echo Importing patients now
for PATIENT_JSON in data/synthea/fhir_r4/*.json; do
	echo importing ${PATIENT_JSON}
	curl http://localhost:8080/baseR4 --data-binary "@${PATIENT_JSON}" -H "Content-Type: application/fhir+json"
done

