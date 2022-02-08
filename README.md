# Data Engineer - Technical Assessment

This is a technical assessment solution to the task provided by EmisGroup for a Developer position.

## Brief task description

Design and prototype a data-pipeline from FHIR standard (json data into tabular csv or sql format)

## Solution formulation

The summary of steps I followed:

1. Explored the provided .json data with the use of json viewers and python coding. 
2. Main areas highlighted: PATIENT, CONDITION, OBSERVATION, MEDICATION, PROCEDURE, ENCOUNTER, CLAIM, and IMMUNIZATION.
3. Brainstormed on how to convert this complex json data into tabular form with pandas.
4. Took a step back and researched into the FHIR standard and understand ETL pipelines.
5. Discovered the [FL7FHIR Resources](https://github.com/nazrulworld/fhir.resources) and made sense of the example codes which helped me to breakdown the problem further.
6. Produced an MVP following discovered examples that allowed me to slice the data into csv form (PATIENT, CONDITION, OBSERVATION, MEDICATION, PROCEDURE, ENCOUNTER, CLAIM and IMMUNIZATION).
7. Added a feature to export the dataframe to_sql split into separate tables with primary and foreign keys.
8. Query SQL tables to check if the scripts was successful.
9. Provide a docker-compose solution.

## Libraries/Tools used

-pandas
-json
-tqdm (Unfortunately will not display properly in docker-compose environment)
-sqlalchemy
-fhir
-docker
-docker-compose

## How to build and run

- `docker build -t python-fhir .`
- `docker-compose up`

Main response
![image](https://user-images.githubusercontent.com/9060307/152896357-0d562d47-b84d-448e-b16a-8dc8dd638a03.png)

Patient .csv example
![image](https://user-images.githubusercontent.com/9060307/152896462-5f9764c4-b425-4522-aed7-f642d7247486.png)

Encounter .csv example
![image](https://user-images.githubusercontent.com/9060307/152896504-ed1614c6-59f3-4cee-8812-2f4b67431aaf.png)


Two docker instances will be ran. First a postgresql instance will be created on port 5432 with database named 'fhir'. Second, a python script will be executed that will transform the .json data into tabular format with pandas that will save each table into .csv files and push the dataframe to_sql.

## Personal reflection

Generally, the assignment was fun, although quite challenging. Although I leveraged my skills in python and postgresql to solve this solution, there were many new techniques, tools and workflows had to be picked up along the way. Therefore, a breakdown of the problem and a lot of structured googling/research was crucial especially due to the time constraint. In order to improve the code, a further discussion would be beneficial to understand the deeper requirements for the data and required features, which could allow on cutting down the code (choice between .csv or sql, graphical features, etc.). 
