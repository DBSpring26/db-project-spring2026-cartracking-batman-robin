# Imported Datasets

fuel_type.parquet
vehicle_kind.parquet
vehicle_status.parquet
vehicle_type.parquet
vehicle.parquet
parking_area.parquet
road_segment.parquet
location_ping.parquet
trip.parquet

# Structure

data_to_import/ 
    ETL/
        db.py 
        import_fuel_type.py 
        import_location_ping.py 
        import_parking_area.py
        import_road_segment.py 
        import_trip.py
        import_vehicle_kind.py 
        import_vehicle_status.py 
        import_vehicle_type.py 
        import_vehicle.py 
        main.py 
        README.md

# Requirements

pip install pandas pyarrow psycopg2-binary

# Credentials

host="dpg-d6ovsu15pdvs739ofrn0-a.virginia-postgres.render.com"
port=5432
dbname="declass"
user="alexisagosto"
password="ehx0AjqfLrNdUErWtDRLgimnorzscTDd"

# ETL

Run main.py, when finished output will be "All Imported".

# Authors

Alexis Agosto Bracetty
Jesus A. Rodríguez Torres