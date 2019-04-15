"""
Variables that define global properties of the module
"""

patient_resources = ['identifier', 'resourceType', 'id', 'active', 'gender', 'name',
                     'birthDate', 'deceased', 'deceased', 'maritalStatus']

condition_resources = ['identifier', 'resourceType', 'id', 'clinicalStatus', 'verificationStatus', 'category',
                       'severity', 'code', 'subject', 'onset']

observation_resources = ['identifier', 'resourceType', 'id', 'status', 'category', 'code', 'subject', 'context',
                         'issued', 'performer', 'value', 'interpretation', 'comment', 'bodySite', 'valueQuantity',
                         'method', 'referenceRange', 'component', 'effectiveDateTime', 'effectivePeriod']

procedure_resources = ['identifier', 'resourceType', 'id', 'subject', 'status', 'notDone', 'notDoneReason', 'category', 'code',
                       'performed', 'reasonCode', 'bodySite', 'outcome', 'report', 'performedPeriod']

date_format = '%Y-%m-%d'
