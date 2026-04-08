from pathlib import Path
from decimal import Decimal
import pandas as pd


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
        speed_kph = None if pd.isna(row["speed_kph"]) else Decimal(str(row["speed_kph"]))
        heading_deg = None if pd.isna(row["heading_deg"]) else Decimal(str(row["heading_deg"]))

        cursor.execute(query, (
            int(row["ping_id"]),
            int(row["vehicle_id"]),
            row["ts"],
            row["geom"],
            speed_kph,
            heading_deg
        ))