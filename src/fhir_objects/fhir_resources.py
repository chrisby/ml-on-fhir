patient_resources = ['identifier', 'resourceType', 'active', 'gender', 'name',
                     'birthDate', 'deceased', 'deceased', 'maritalStatus']

condition_resources = ['identifier', 'resourceType', 'clinicalStatus', 'verificationStatus', 'category',
                     'severity', 'code', 'subject', 'onset']

observation_resources = ['identifier', 'resourceType', 'status', 'category', 'code', 'subject', 'context',
                      'issued', 'performer', 'value', 'interpretation', 'comment', 'bodySite',
                      'method', 'referenceRange', 'component']  

procedure_resources = ['identifier', 'resourceType', 'subject', 'status', 'notDone', 'notDoneReason', 'category', 'code',
                       'performed', 'reasonCode', 'bodySite', 'outcome', 'report', 'performedPeriod']

date_format = '%Y-%m-%d'
