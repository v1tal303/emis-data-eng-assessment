import pandas as pd
from sqlalchemy import create_engine

data = pd.read_csv ('PATIENT.csv')
df = pd.DataFrame(data)

df.name = "test"

print(df)
# engine = create_engine('postgresql://postgres:password@localhost:5432/fhir')
#
# df.to_sql(name="patients", con=engine, if_exists="replace", index=False)
#
# with engine.connect() as con:
#     con.execute('ALTER TABLE patients ADD PRIMARY KEY ("PatientUID");')
#
# print("Database has been created successfully !!")

