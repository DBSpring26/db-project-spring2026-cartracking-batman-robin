from pathlib import Path
import pandas as pd
from db import get_connection

def import_trip(cursor):
    file_path = Path(__file__).resolve().parent.parent / "trip.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.trip (
        trip_id,
        vehicle_id,
        start_ts,
        end_ts,
        start_geom,
        end_geom,
        distance_km
    )
    VALUES (
        %s,
        %s,
        %s,
        %s,
        ST_GeomFromEWKB(decode(%s, 'hex')),
        ST_GeomFromEWKB(decode(%s, 'hex')),
        %s
    )
    ON CONFLICT (trip_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["trip_id"]),
            int(row["vehicle_id"]),
            row["start_ts"],
            row["end_ts"],
            row["start_geom"],
            row["end_geom"],
            float(row["distance_km"])
        ))
