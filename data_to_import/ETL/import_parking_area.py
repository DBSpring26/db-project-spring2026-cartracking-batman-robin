from pathlib import Path
import pandas as pd
from db import get_connection

def import_parking_area(cursor):
    file_path = Path(__file__).resolve().parent.parent / "parking_area.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.parking_area (
        parking_area_id,
        name,
        capacity,
        geom,
        created_at
    )
    VALUES (%s, %s, %s, ST_GeomFromEWKB(decode(%s, 'hex')), %s)
    ON CONFLICT (parking_area_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["parking_area_id"]),
            row["name"],
            int(row["capacity"]),
            row["geom"],
            row["created_at"]
        ))
