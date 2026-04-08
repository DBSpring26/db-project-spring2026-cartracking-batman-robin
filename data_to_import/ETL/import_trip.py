from pathlib import Path
from decimal import Decimal
import pandas as pd


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
        distance_km = None if pd.isna(row["distance_km"]) else Decimal(str(row["distance_km"]))

        cursor.execute(query, (
            int(row["trip_id"]),
            int(row["vehicle_id"]),
            row["start_ts"],
            row["end_ts"],
            row["start_geom"],
            row["end_geom"],
            distance_km
        ))