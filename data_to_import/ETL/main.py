from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent
file_path = base_dir.parent / "trip.parquet"

print(file_path)

df = pd.read_parquet(file_path)

print(df.columns.tolist())
print(df.head())