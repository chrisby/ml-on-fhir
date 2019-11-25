# ml-on-fhir

## A work in progress library that fuses the HL7 FHIR standard with scikit-learn

Read more about internals and extendability in the [readthedocs](https://ml-on-fhir.readthedocs.io/en/latest/).

### Usage (taken from [our demo notebook](https://github.com/chrisby/ml-on-fhir/blob/master/src/Demo.ipynb))

##### First: Register the base URL of your database with a FHIRCient object:

```python
from fhir_client import FHIRClient
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = FHIRClient(service_base_url='https://r3.smarthealthit.org', logger=None)
```

##### Querying Patients
There are two general ways of searching for patients with specific properties.
The first one is to search by coding system:
```python
procedures = client.get_all_procedures()
pd.DataFrame([prod.code['coding'][0] for prod in procedures]).drop_duplicates().sort_values(by=['display']).head()
```

The second one is by text. The searched text will be CodeableConcept.text, Coding.display, or Identifier.type.text:
```python
conditions = client.get_all_conditions()
pd.DataFrame([cond.code['coding'][0] for cond in conditions]).drop_duplicates(subset=['display']).sort_values(by='display', ascending=True).head()
```

One can also load a control group for a specific cohort of patients. The control group is of equal size of the case cohort (min size: 10) and is composed of randomly sampled patients that do not match the original query. Their class is contained in the .case property of the Patient object.
```python
patients_by_condition_text_with_controls = client.get_patients_by_condition_text("Abdominal pain", controls=True)
print("Retrieved {} patients with a total of {} observations".format( len(patients_by_condition_text_with_controls), 
                                                               sum([len(pat.observations) for pat in patients_by_condition_text_with_controls])))
print("{} are cases and {} are controls".format(len([d for d in patients_by_condition_text_with_controls if d.case]), 
                                                len([d for d in patients_by_condition_text_with_controls if not d.case])))
```

#### Machine Learning
In a nutshell: 
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
