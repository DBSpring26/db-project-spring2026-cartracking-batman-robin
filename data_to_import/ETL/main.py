from pathlib import Path
import pandas as pd
from db import get_connection

base_dir = Path(__file__).resolve().parent
file_path = base_dir.parent / "vehicle_type.parquet"

df = pd.read_parquet(file_path)

conn = get_connection()
cursor = conn.cursor()

print("Importing vehicle_type...")

for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO public.vehicle_type 
        (id, vehicle_kind_id, fuel_type_id, emissions_rating, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """,
        (
            int(row["id"]),
            int(row["vehicle_kind_id"]),
            int(row["fuel_type_id"]),
            float(row["emissions_rating"]),
            row["created_at"]
        )
    )

conn.commit()
cursor.close()
conn.close()

print("All Imported.")