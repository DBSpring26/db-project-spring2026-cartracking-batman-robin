from pathlib import Path
import pandas as pd
from db import get_connection

def import_vehicle_status(cursor):
    file_path = Path(__file__).resolve().parent.parent / "vehicle_status.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.vehicle_status (
        vehicle_status_id,
        name
    )
    VALUES (%s, %s)
    ON CONFLICT (vehicle_status_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["vehicle_status_id"]),
            row["name"]
        ))
