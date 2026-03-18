from pathlib import Path
import pandas as pd
from db import get_connection

def import_location_ping(cursor):
    file_path = Path(__file__).resolve().parent.parent / "location_ping.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.location_ping (
        ping_id,
        vehicle_id,
        ts,
        geom,
        speed_kph,
        heading_deg
    )
    VALUES (%s, %s, %s, ST_GeomFromEWKB(decode(%s, 'hex')), %s, %s)
    ON CONFLICT (ping_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["ping_id"]),
            int(row["vehicle_id"]),
            row["ts"],
            row["geom"],
            float(row["speed_kph"]) if pd.notna(row["speed_kph"]) else None,
            float(row["heading_deg"]) if pd.notna(row["heading_deg"]) else None
        ))
