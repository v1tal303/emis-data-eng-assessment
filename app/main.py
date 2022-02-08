import os
import pandas as pd
import json
import sqlalchemy
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import psycopg2

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

Allfiles = os.listdir('./data')
print(f"Discovered: {len(Allfiles)} files")

# Initialize pandas dataframes

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

# Use tqdm bar to show progress.

for fileNum in tqdm(range(len(Allfiles))):
    f = open('./data/'+Allfiles[fileNum], encoding="utf8")
    json_obj = json.load(f)

    oneBundle = Bundle.parse_obj(json_obj)

    # Resources
    resources = []
    if oneBundle.entry is not None:
        for entry in oneBundle.entry:
            resources.append(entry.resource)

    onePatient = Patient.parse_obj(resources[0])

    # Patient demographics
    onePatientID = onePatient.id

    PATIENT.loc[len(PATIENT.index)] = [onePatientID, onePatient.name[0].family,
                                       onePatient.name[0].given[0], onePatient.birthDate, onePatient.gender]

    # Find Condition resources
    resCondition = []
    for j in range(len(resources)):
        if resources[j].__class__.__name__ == 'Condition':
            resCondition.append(resources[j])

    conditions = []
    conditionOnsetDates = []
    for j in range(len(resCondition)):
        oneCondition = Condition.parse_obj(resCondition[j])
        conditions.append(oneCondition.code.text)
        conditionOnsetDates.append(str(oneCondition.onsetDateTime.date()))

    onePatConditions = pd.DataFrame()

    onePatConditions['ConditionText'] = conditions
    onePatConditions['ConditionOnsetDates'] = conditionOnsetDates
    onePatConditions['PatientUID'] = onePatientID

    CONDITION = pd.concat([CONDITION, onePatConditions], ignore_index=True, axis=0)
    CONDITION.reset_index()

    # Find Observation resources
    resObservation = []
    for j in range(len(resources)):
        if resources[j].__class__.__name__ == 'Observation':
            resObservation.append(resources[j])

    obsText = []
    obsValue = []
    obsUnit = []
    obsDate = []

    for j in range(len(resObservation)):
        oneObservation = Observation.parse_obj(resObservation[j])
        obsText.append(oneObservation.code.text)
        if oneObservation.valueQuantity:
            obsValue.append(round(oneObservation.valueQuantity.value, 2))
            obsUnit.append(oneObservation.valueQuantity.unit)
        else:
            obsValue.append('None')
            obsUnit.append('None')
        obsDate.append(oneObservation.issued.date())

    onePatObs = pd.DataFrame()

    onePatObs['ObservationText'] = obsText
    onePatObs['ObservationValue'] = obsValue
    onePatObs['ObservationUnit'] = obsUnit
    onePatObs['ObservationDate'] = obsDate
    onePatObs['PatientUID'] = onePatientID

    OBSERVATION = pd.concat([OBSERVATION, onePatObs], ignore_index=True, axis=0)
    OBSERVATION.reset_index()

    # Find Medication resources
    resMedicationRequest = []
    for j in range(len(resources)):
        if resources[j].__class__.__name__ == 'MedicationRequest':
            resMedicationRequest.append(resources[j])

    meds = []
    medsDates = []
    for j in range(len(resMedicationRequest)):
        oneMed = MedicationRequest.parse_obj(resMedicationRequest[j])
        try:
            meds.append(oneMed.medicationCodeableConcept.text)
            medsDates.append(str(oneMed.authoredOn.date()))
        except AttributeError:
            pass

    onePatMeds = pd.DataFrame()

    onePatMeds['MedicationText'] = meds
    onePatMeds['MedicationDates'] = medsDates
    onePatMeds['PatientUID'] = onePatientID

    MEDICATION = pd.concat([MEDICATION, onePatMeds], ignore_index=True, axis=0)
    MEDICATION.reset_index()

    # Find Procedure resources
    resProcedures = []
    for j in range(len(resources)):
        if resources[j].__class__.__name__ == 'Procedure':
            resProcedures.append(resources[j])

    procs = []
    procDates = []
    for j in range(len(resProcedures)):
        oneProc = Procedure.parse_obj(resProcedures[j])
        procs.append(oneProc.code.text)
        procDates.append(str(oneProc.performedPeriod.start.date()))

    onePatProcs = pd.DataFrame()

    onePatProcs['ProcedureText'] = procs
    onePatProcs['ProcedureDates'] = procDates
    onePatProcs['PatientUID'] = onePatientID

    PROCEDURE = pd.concat([PROCEDURE, onePatProcs], ignore_index=True, axis=0)
    PROCEDURE.reset_index()

    # Find Encounter resources
    resEncounters = []
    for j in range(len(resources)):
        if resources[j].__class__.__name__ == 'Encounter':
            resEncounters.append(resources[j])

    encounters = []
    encountDates = []
    encountLocation = []
    encountProvider = []

    for j in range(len(resEncounters)):
        oneEncounter = Encounter.parse_obj(resEncounters[j])
        encounters.append(oneEncounter.type[0].text)
        encountLocation.append(oneEncounter.serviceProvider.display)
        if oneEncounter.participant:
            encountProvider.append(oneEncounter.participant[0].individual.display)
        else:
            encountProvider.append('None')
        encountDates.append(str(oneEncounter.period.start.date()))

    onePatEncounters = pd.DataFrame()

    onePatEncounters['EncountersText'] = encounters
    onePatEncounters['EncounterLocation'] = encountLocation
    onePatEncounters['EncounterProvider'] = encountProvider
    onePatEncounters['EncounterDates'] = encountDates
    onePatEncounters['PatientUID'] = onePatientID

    ENCOUNTER = pd.concat([ENCOUNTER, onePatEncounters], ignore_index=True, axis=0)
    ENCOUNTER.reset_index()

    # Find Claim resources
    resClaims = []
    for j in range(len(resources)):
        if resources[j].__class__.__name__ == 'Claim':
            resClaims.append(resources[j])

    claimProvider = []
    claimInsurance = []
    claimDate = []
    claimType = []
    claimItem = []
    claimUSD = []

    for j in range(len(resClaims)):
        oneClaim = Claim.parse_obj(resClaims[j])
        # Inner loop over claim items:
        for i in range(len(resClaims[j].item)):
            claimProvider.append(oneClaim.provider.display)
            claimInsurance.append(oneClaim.insurance[0].coverage.display)
            claimDate.append(str(oneClaim.billablePeriod.start.date()))
            claimType.append(oneClaim.type.coding[0].code)
            claimItem.append(resClaims[j].item[i].productOrService.text)
            if resClaims[j].item[i].net:
                claimUSD.append(str(resClaims[j].item[i].net.value))
            else:
                claimUSD.append('None')

    onePatClaims = pd.DataFrame()

    onePatClaims['ClaimProvider'] = claimProvider
    onePatClaims['ClaimInsurance'] = claimInsurance
    onePatClaims['ClaimDate'] = claimDate
    onePatClaims['ClaimType'] = claimType
    onePatClaims['ClaimItem'] = claimItem
    onePatClaims['ClaimUSD'] = claimUSD
    onePatClaims['PatientUID'] = onePatientID

    CLAIM = pd.concat([CLAIM, onePatClaims], ignore_index=True, axis=0)
    CLAIM.reset_index()

    # Find Immunization resources
    resImmunization = []
    for j in range(len(resources)):
        if resources[j].__class__.__name__ == 'Immunization':
            resImmunization.append(resources[j])

    immun = []
    immunDates = []
    for j in range(len(resImmunization)):
        oneImmun = Immunization.parse_obj(resImmunization[j])
        immun.append(oneImmun.vaccineCode.coding[0].display)
        immunDates.append(str(oneImmun.occurrenceDateTime.date()))

    onePatImmun = pd.DataFrame()

    onePatImmun['Immunization'] = immun
    onePatImmun['ImmunizationDates'] = immunDates
    onePatImmun['PatientUID'] = onePatientID

    IMMUNIZATION = pd.concat([IMMUNIZATION, onePatImmun], ignore_index=True, axis=0)
    IMMUNIZATION.reset_index()

# Save the tables created

PATIENT.to_csv('PATIENT.csv', index=False)
CONDITION.to_csv('CONDITION.csv', index=False)
OBSERVATION.to_csv('OBSERVATION.csv', index=False)
MEDICATION.to_csv('MEDICATION.csv', index=False)
PROCEDURE.to_csv('PROCEDURE.csv', index=False)
ENCOUNTER.to_csv('ENCOUNTER.csv', index=False)
CLAIM.to_csv('CLAIM.csv', index=False)
IMMUNIZATION.to_csv('IMMUNIZATION.csv', index=False)

# Add name to all the dataframes for reference

PATIENT.name = "patient"
CONDITION.name = "condition"
OBSERVATION.name = "observation"
MEDICATION.name = "medication"
PROCEDURE.name = "procedure"
ENCOUNTER.name = "encounter"
CLAIM.name = "claim"
IMMUNIZATION.name = "immunization"

table_list = [PATIENT, CONDITION, OBSERVATION, MEDICATION, PROCEDURE, ENCOUNTER, CLAIM, IMMUNIZATION]

# Establish a postgresql connection

engine = create_engine('postgresql://postgres:password@db:5432/fhir')
con = engine.connect()


# Clear database if exists (if the tables have been created previously an primary key error will be raised)

for i in table_list:
    con.execute(f'DROP TABLE IF EXISTS {i.name} CASCADE;')

# Add the dataframe to db

for i in table_list:
    i.to_sql(name=str(i.name), con=engine, if_exists="replace", index=False)

# Add primary and foreign keys

con.execute('ALTER TABLE patient ADD PRIMARY KEY ("PatientUID");')
for i in table_list[1:]:
    con.execute(f'ALTER TABLE {i.name} ADD CONSTRAINT fk_PUID FOREIGN KEY ("PatientUID") REFERENCES patient ('
                f'"PatientUID");')

print("DB fhir created successfully")

# Check the created tables

for i in table_list:
    print(f"5 ROWS FROM TABLE: {i.name}")
    print("____________________________")
    sqlresult = con.execute(f'SELECT * FROM {i.name} LIMIT 5;')
    print(sqlresult.fetchall())
    print("____________________________")
print("All tables have also been saved as .csv files")