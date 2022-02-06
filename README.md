# Data Engineer - Technical Assesment

This is a technical assessment solution to the task provided by EmisGroup for a Developer position.

## Brief task description

Design and prototype a data-pipeline from FHIR standard.

## Solution formulation

The summary of steps I followed (WIP):

1. Explored the provided .json data with the use of json viewers and python coding. 
2. Main areas highlighted: PATIENT, CONDITION, OBSERVATION, MEDICATION, PROCEDURE, ENCOUNTER, CLAIM and IMMUNIZATION.
3. Brainstormed on how to convert this complex json data into tabular form with pandas.
4. Took a step back and and researched into the FHIR standard and understand ETL pipelines.
5. Discovered the [FL7FHIR Resources](https://github.com/nazrulworld/fhir.resources) and made sense of the example codes which helped me to breakdown the problem further.
6. Produced a MVP to slice the data into csv form (PATIENT, CONDITION, OBSERVATION, MEDICATION, PROCEDURE, ENCOUNTER, CLAIM and IMMUNIZATION)
7. Added a feature to export the dataframe to_sql split into seperate tables with primary and foreign keys
8. Provide a docker image(WIP)

## Libraries/Tools used

-pandas
-json
-tqdm
-sqlalchemy
-fhir

## How to setup


## Running images


## Decisions and tradeoffs


## Notes

