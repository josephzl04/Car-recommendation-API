import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "dataset" / "vehicles.csv"

df = pd.read_csv(csv_path, nrows=1000)
print(df.columns)
print(df.head())
print(len(df))