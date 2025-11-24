import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

files = glob.glob("states*.csv")

df_list = []
for filename in files:
  data = pd.read_csv(filename)
  df_list.append(data)
us_census = pd.concat(df_list)

print(us_census.head())

percent_cols = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
for col in percent_cols:
    us_census[col] = us_census[col].str.rstrip('%').astype(float)
us_census['Income'] = us_census['Income'].str.replace('$', '', regex=False).astype(float)
us_census[['Men', 'Women']] = us_census['GenderPop'].str.split('_', expand=True)
us_census['Men'] = us_census['Men'].str.rstrip('M').astype(float)
us_census['Women'] = pd.to_numeric(us_census['Women'].str.rstrip('F'), errors='coerce')
us_census = us_census.drop(columns=['Unnamed: 0'])

print(us_census.head())

plt.scatter(us_census['Women'], us_census['Income'])
plt.show()

us_census['Women'] = us_census['Women'].fillna(us_census['TotalPop'] - us_census['Men'])
print(us_census['Women'])

print(us_census.duplicated().sum())
print(us_census[us_census.duplicated()])
us_census = us_census.drop_duplicates()
print(us_census.duplicated().sum())

plt.scatter(us_census['Women'], us_census['Income'])
plt.show()

print(us_census[percent_cols].isna().sum())
for col in percent_cols:
    us_census[col].fillna(us_census[col].mean(), inplace=True)

for col in percent_cols:
    plt.hist(us_census[col])
    plt.title(col + " Distribution")
    plt.xlabel(col + " (%)")
    plt.ylabel("Frequency")
    plt.show()