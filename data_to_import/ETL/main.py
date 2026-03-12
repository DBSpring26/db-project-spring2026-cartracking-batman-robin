from pathlib import Path
import pandas as pd
from db import get_connection


def import_trip(cursor):
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "trip.parquet"

    df = pd.read_parquet(file_path)

    print(file_path)
    print(df.columns.tolist())
    print(df.head())

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
            row["trip_id"],
            row["vehicle_id"],
            row["start_ts"],
            row["end_ts"],
            row["start_geom"],
            row["end_geom"],
            row["distance_km"]
        ))


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        import_trip(cursor)
        conn.commit()
        print("Trip imported.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()