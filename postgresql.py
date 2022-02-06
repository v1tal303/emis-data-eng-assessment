import psycopg2
import pandas as pd
from sqlalchemy import create_engine

data = pd.read_csv ('PATIENT.csv')
df = pd.DataFrame(data)


print(df)

conn = psycopg2.connect(
   database="fhir",
    user='postgres',
    password='password',
    host='localhost',
    port= '5432'
)

conn.autocommit = True

# Creating a cursor object
cursor = conn.cursor()

# query to create a database
# sql = ''' CREATE database fhir '''

# cursor.execute('''
# 		CREATE TABLE patient (
# 			PatientUID varchar(50) primary key,
# 			NameFamily varchar(50),
# 			NameGiven varchar(50),
# 			DoB DATE,
# 			Gender varchar(50))
#                ''')

engine = create_engine('postgresql://postgres:password@localhost:5432/fhir')

df.to_sql("patients2", engine, index=False)

conn.commit()

# executing above query
# cursor.execute(sql)
print("Database has been created successfully !!")

# Closing the connection
conn.close()