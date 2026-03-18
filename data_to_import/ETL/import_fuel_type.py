from pathlib import Path
import pandas as pd


def import_fuel_type(cursor):
    file_path = Path(__file__).resolve().parent.parent / "fuel_type.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.fuel_type (
        fuel_type_id,
        name
    )
    VALUES (%s, %s)
    ON CONFLICT (fuel_type_id) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            int(row["fuel_type_id"]),
            row["name"]
        ))