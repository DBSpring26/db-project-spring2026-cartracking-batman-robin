from pathlib import Path
import pandas as pd


def import_road_segment(cursor):
    file_path = Path(__file__).resolve().parent.parent / "road_segment.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.road_segment (
        road_id,
        name,
        speed_limit_kph,
        geom,
        created_at,
        is_oneway,
        direction
    )
    VALUES (%s, %s, %s, ST_GeomFromEWKB(decode(%s, 'hex')), %s, %s, %s)
    ON CONFLICT (road_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["road_id"]),
            row["name"],
            int(row["speed_limit_kph"]),
            row["geom"],
            row["created_at"],
            bool(row["is_oneway"]),
            row["direction"]
        ))