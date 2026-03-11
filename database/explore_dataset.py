import pandas as pd

df = pd.read_csv("dataset/vehicles.csv", nrows=1000)
print(df.columns)
print(df.head())
print(len(df))