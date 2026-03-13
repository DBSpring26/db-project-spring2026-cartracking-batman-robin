from pathlib import Path
import pandas as pd
from db import get_connection


def import_vehicle_kind(cursor):
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "vehicle_kind.parquet"

    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.vehicle_kind (
        vehicle_kind_id,
        name
    )
    VALUES (%s,%s)
    ON CONFLICT (vehicle_kind_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            row["vehicle_kind_id"],
            row["name"]
        ))


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Importing vehicle_kind...")
        import_vehicle_kind(cursor)

        conn.commit()
        print("All Imported")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()