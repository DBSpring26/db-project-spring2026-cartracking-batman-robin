from pathlib import Path
import pandas as pd
from db import get_connection


def import_vehicle(cursor):

    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "vehicle.parquet"

    df = pd.read_parquet(file_path)

    print(file_path)
    print(df.columns.tolist())
    print(df.head())

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


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        import_vehicle(cursor)
        conn.commit()
        print("Vehicle importate")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()