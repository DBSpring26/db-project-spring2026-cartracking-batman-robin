from pathlib import Path
from decimal import Decimal
import pandas as pd


def import_vehicle_type(cursor):
    file_path = Path(__file__).resolve().parent.parent / "vehicle_type.parquet"
    df = pd.read_parquet(file_path)

    query = """
    INSERT INTO public.vehicle_type (
        id,
        vehicle_kind_id,
        fuel_type_id,
        emissions_rating,
        created_at
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    for _, row in df.iterrows():
        emissions_rating = None if pd.isna(row["emissions_rating"]) else Decimal(str(row["emissions_rating"]))

        cursor.execute(query, (
            int(row["id"]),
            int(row["vehicle_kind_id"]),
            int(row["fuel_type_id"]),
            emissions_rating,
            row["created_at"]
        ))