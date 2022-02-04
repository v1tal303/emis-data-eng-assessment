import pandas as pd
import glob
import json

path = r'C:\Users\murci\Documents\GitHub\emis-data-eng-assessment\data'
all_files = glob.glob(path + "/*.json")

print(all_files[0])

data = pd.read_json(all_files[0])

print(data)

# for i in all_files:
#     data = json.load(open(path, "r"))
#     print(data[0][0])