from import_fuel_type import import_fuel_type
from import_vehicle_kind import import_vehicle_kind
from import_vehicle_status import import_vehicle_status
from import_vehicle_type import import_vehicle_type
from import_vehicle import import_vehicle
from import_parking_area import import_parking_area
from import_road_segment import import_road_segment
from import_location_ping import import_location_ping
from import_trip import import_trip
from db import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("Importing fuel_type...")
        import_fuel_type(cursor)

        print("Importing vehicle_kind...")
        import_vehicle_kind(cursor)

        print("Importing vehicle_status...")
        import_vehicle_status(cursor)

        print("Importing vehicle_type...")
        import_vehicle_type(cursor)

        print("Importing vehicle...")
        import_vehicle(cursor)

        print("Importing parking_area...")
        import_parking_area(cursor)

        print("Importing road_segment...")
        import_road_segment(cursor)

        print("Importing location_ping...")
        import_location_ping(cursor)

        print("Importing trip...")
        import_trip(cursor)

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