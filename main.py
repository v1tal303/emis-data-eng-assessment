import os
import pandas as pd
import json
from tqdm.auto import tqdm

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


