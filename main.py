import os
import pandas as pd
import json
from tqdm.auto import tqdm

from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.condition import Condition
from fhir.resources.observation import Observation
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.procedure import Procedure
from fhir.resources.encounter import Encounter
from fhir.resources.claim import Claim
from fhir.resources.immunization import Immunization

tqdm.pandas()

# Get all the .json files from the directory below

Allfiles = os.listdir('/Users/murci/Documents/GitHub/emis-data-eng-assessment/data')
print(len(Allfiles))
print(Allfiles)

# Initialize pandas df

PATIENT = pd.DataFrame(columns=['PatientUID', 'NameFamily', 'NameGiven', 'DoB', 'Gender'])
CONDITION = pd.DataFrame(columns=['ConditionText', 'ConditionOnsetDates', 'PatientUID'])
OBSERVATION = pd.DataFrame(columns=['ObservationText', 'ObservationValue', 'ObservationUnit',
                                    'ObservationDate', 'PatientUID'])
MEDICATION = pd.DataFrame(columns=['MedicationText', 'MedicationDates', 'PatientUID'])
PROCEDURE = pd.DataFrame(columns=['ProcedureText', 'ProcedureDates', 'PatientUID'])
ENCOUNTER = pd.DataFrame(
    columns=['EncountersText', 'EncounterLocation', 'EncounterProvider', 'EncounterDates', 'PatientUID'])
CLAIM = pd.DataFrame(columns=['ClaimProvider', 'ClaimInsurance', 'ClaimDate', 'ClaimType', 'ClaimItem',
                              'ClaimUSD', 'PatientUID'])
IMMUNIZATION = pd.DataFrame(columns=['Immunization', 'ImmunizationDates', 'PatientUID'])



for fileNum in tqdm(range(len(Allfiles))):
    f = open('/Users/murci/Documents/GitHub/emis-data-eng-assessment/data/'+Allfiles[fileNum], encoding="utf8")
    json_obj = json.load(f)

    singleBundle = Bundle.parse_obj(json_obj)

    # Resources
    resources = []
    if singleBundle.entry is not None:
        for entry in singleBundle.entry:
            resources.append(entry.resource)

    singlePatient = Patient.parse_obj(resources[0])



