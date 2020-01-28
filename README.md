# ml-on-fhir

## A work in progress library that fuses the HL7 FHIR standard with scikit-learn

Currently this library is only tested on `STU3`, so use with caution when you run a R4 database. We will look more into compatibility checks in the future. 

Read more about internals and extendability in the [readthedocs](https://ml-on-fhir.readthedocs.io/en/latest/).

### Usage (taken from [our demo notebook](https://github.com/chrisby/ml-on-fhir/blob/master/src/Demo.ipynb))

##### First: Register the base URL of your database with a FHIRCient object:

```python
from fhir_client import FHIRClient
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = FHIRClient(service_base_url='https://r3.smarthealthit.org', logger=logger)
```

##### Querying Patients
There are two general ways of searching for patients with specific properties.
The first one is to search by coding system:
```python
# To receive a list of available procedures:
procedures = client.get_all_procedures()
pd.DataFrame([prod.code['coding'][0] for prod in procedures]).drop_duplicates().sort_values(by=['display']).head()

# Now retrieve patients
patients_by_procedure_code = client.get_patients_by_procedure_code("http://snomed.info/sct","73761001")
```

The second one is by text. The searched tags are CodeableConcept.text, Coding.display, or Identifier.type.text:
```python
conditions = client.get_all_conditions()
pd.DataFrame([cond.code['coding'][0] for cond in conditions]).drop_duplicates(subset=['display']).sort_values(by='display', ascending=True).head()

patients_by_condition_text = client.get_patients_by_condition_text("Abdominal pain")
```

One can also load a control group for a specific cohort of patients. The control group is of equal size of the case cohort (min size: 10) and is composed of randomly sampled patients that do not match the original query. Their class is contained in the .case property of the Patient object.
```python
patients_by_condition_text_with_controls = client.get_patients_by_condition_text("Abdominal pain", controls=True)

print("{} are cases and {} are controls".format(len([d for d in patients_by_condition_text_with_controls if d.case]), 
                                                len([d for d in patients_by_condition_text_with_controls if not d.case])))
```

#### Machine Learning
To train a classifier, we need to first tell the `MLOnFHIRClassifier` the type of object which we would like to classify. We can then define features (`feature_attrs`) and labels (`label_attrs`) for our classification task and pass the preprocessor of our current client, so it is clear how to preprocess the features/labels of a patient. We can then simply call `.fit` on the `MLOnFHIRClassifier` instance together with our classifier of choice.

```python
from ml_on_fhir import MLOnFHIRClassifier
from fhir_objects.patient import Patient
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_curve, auc

ml_fhir = MLOnFHIRClassifier(Patient, feature_attrs=['birthDate', 'gender'],
                             label_attrs=['case'], preprocessor=client.preprocessor)
X, y, trained_clf = ml_fhir.fit(patients_by_condition_text_with_controls, DecisionTreeClassifier())

from sklearn.metrics import accuracy_score, roc_curve, auc
fpr, tpr, _ = roc_curve(y, trained_clf.predict(X))
print("Prediction accuracy {}".format( auc(fpr, tpr) ) )
```
