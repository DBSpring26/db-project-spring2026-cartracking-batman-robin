from pathlib import Path
import pandas as pd


def import_vehicle_kind(cursor):
    file_path = Path(__file__).resolve().parent.parent / "vehicle_kind.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.vehicle_kind (
        vehicle_kind_id,
        name
    )
    VALUES (%s, %s)
    ON CONFLICT (vehicle_kind_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["vehicle_kind_id"]),
            row["name"]
        ))