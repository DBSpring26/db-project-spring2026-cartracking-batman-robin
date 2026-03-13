from pathlib import Path
import pandas as pd
from db import get_connection


def import_vehicle(cursor):
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "vehicle.parquet"

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
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (vehicle_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            row["vehicle_id"],
            row["vehicle_type_id"],
            row["vehicle_status_id"],
            row["plate_number"],
            row["make"],
            row["model"],
            row["year"],
            row["created_at"]
        ))


def import_parking_area(cursor):
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "parking_area.parquet"

    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.parking_area (
        parking_area_id,
        name,
        capacity,
        geom,
        created_at
    )
    VALUES (%s,%s,%s,ST_GeomFromEWKB(decode(%s,'hex')),%s)
    ON CONFLICT (parking_area_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            row["parking_area_id"],
            row["name"],
            row["capacity"],
            row["geom"],
            row["created_at"]
        ))


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Importing vehicle...")
        import_vehicle(cursor)

        print("Importing parking_area...")
        import_parking_area(cursor)

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