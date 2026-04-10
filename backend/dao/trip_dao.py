class TripDAO:
    def __init__(self, conn):
        self.conn = conn

    def vehicle_exists(self, vehicle_id: int) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM public.vehicle WHERE vehicle_id = %s;",
                (vehicle_id,)
            )
            return cursor.fetchone() is not None

    def create_trip(self, data: dict):
        start_lon, start_lat = data["start_geom"]["coordinates"]
        end_lon, end_lat = data["end_geom"]["coordinates"]

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.trip (
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
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    %s
                )
                RETURNING
                    trip_id,
                    vehicle_id,
                    start_ts,
                    end_ts,
                    ST_AsGeoJSON(start_geom)::json AS start_geom,
                    ST_AsGeoJSON(end_geom)::json AS end_geom,
                    distance_km;
                """,
                (
                    data["vehicle_id"],
                    data["start_ts"],
                    data["end_ts"],
                    start_lon,
                    start_lat,
                    end_lon,
                    end_lat,
                    data["distance_km"],
                )
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_trips(self, limit: int, offset: int, vehicle_id=None, start_date=None, end_date=None):
        query = """
            SELECT
                trip_id,
                vehicle_id,
                start_ts,
                end_ts,
                ST_AsGeoJSON(start_geom)::json AS start_geom,
                ST_AsGeoJSON(end_geom)::json AS end_geom,
                distance_km
            FROM public.trip
            WHERE 1=1
        """
        params = []

        if vehicle_id is not None:
            query += " AND vehicle_id = %s"
            params.append(vehicle_id)

        if start_date is not None:
            query += " AND start_ts >= %s"
            params.append(start_date)

        if end_date is not None:
            query += " AND end_ts <= %s"
            params.append(end_date)

        query += " ORDER BY trip_id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = "SELECT COUNT(*) AS total FROM public.trip WHERE 1=1"
            count_params = []

            if vehicle_id is not None:
                count_query += " AND vehicle_id = %s"
                count_params.append(vehicle_id)

            if start_date is not None:
                count_query += " AND start_ts >= %s"
                count_params.append(start_date)

            if end_date is not None:
                count_query += " AND end_ts <= %s"
                count_params.append(end_date)

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }

    def get_trip_by_id(self, trip_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    trip_id,
                    vehicle_id,
                    start_ts,
                    end_ts,
                    ST_AsGeoJSON(start_geom)::json AS start_geom,
                    ST_AsGeoJSON(end_geom)::json AS end_geom,
                    distance_km
                FROM public.trip
                WHERE trip_id = %s;
                """,
                (trip_id,)
            )
            return cursor.fetchone()

    def update_trip(self, trip_id: int, data: dict):
        fields = []
        values = []

        for key, value in data.items():
            if key == "start_geom":
                lon, lat = value["coordinates"]
                fields.append("start_geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326)")
                values.extend([lon, lat])
            elif key == "end_geom":
                lon, lat = value["coordinates"]
                fields.append("end_geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326)")
                values.extend([lon, lat])
            else:
                fields.append(f"{key} = %s")
                values.append(value)

        values.append(trip_id)

        query = f"""
            UPDATE public.trip
            SET {", ".join(fields)}
            WHERE trip_id = %s
            RETURNING
                trip_id,
                vehicle_id,
                start_ts,
                end_ts,
                ST_AsGeoJSON(start_geom)::json AS start_geom,
                ST_AsGeoJSON(end_geom)::json AS end_geom,
                distance_km;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def delete_trip(self, trip_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM public.trip WHERE trip_id = %s RETURNING trip_id;",
                (trip_id,)
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_vehicle_trips(self, vehicle_id: int, limit: int, offset: int, start_date=None, end_date=None):
        query = """
            SELECT
                trip_id,
                start_ts,
                end_ts,
                ST_AsGeoJSON(start_geom)::json AS start_geom,
                ST_AsGeoJSON(end_geom)::json AS end_geom,
                distance_km
            FROM public.trip
            WHERE vehicle_id = %s
        """
        params = [vehicle_id]

        if start_date is not None:
            query += " AND start_ts >= %s"
            params.append(start_date)

        if end_date is not None:
            query += " AND end_ts <= %s"
            params.append(end_date)

        query += " ORDER BY start_ts DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = "SELECT COUNT(*) AS total FROM public.trip WHERE vehicle_id = %s"
            count_params = [vehicle_id]

            if start_date is not None:
                count_query += " AND start_ts >= %s"
                count_params.append(start_date)

            if end_date is not None:
                count_query += " AND end_ts <= %s"
                count_params.append(end_date)

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "vehicle_id": vehicle_id,
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }