from pathlib import Path
import pandas as pd
from db import get_connection


def import_location_ping(cursor):
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "location_ping.parquet"

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
    VALUES (%s,%s,%s,ST_GeomFromEWKB(decode(%s,'hex')),%s,%s)
    ON CONFLICT (ping_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            row["ping_id"],
            row["vehicle_id"],
            row["ts"],
            row["geom"],
            row["speed_kph"],
            row["heading_deg"]
        ))


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Importing location_ping...")
        import_location_ping(cursor)

        conn.commit()
        print("All Imported.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()