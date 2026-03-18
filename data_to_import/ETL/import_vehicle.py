from pathlib import Path
import pandas as pd
from db import get_connection

def import_vehicle(cursor):
    file_path = Path(__file__).resolve().parent.parent / "vehicle.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.vehicle (
        vehicle_id,
        vehicle_type_id,
        vehicle_status_id,
        plate_number,
        make,
        model,
        year,
        created_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (vehicle_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["vehicle_id"]),
            int(row["vehicle_type_id"]),
            int(row["vehicle_status_id"]),
            row["plate_number"],
            row["make"],
            row["model"],
            int(row["year"]),
            row["created_at"]
        ))
