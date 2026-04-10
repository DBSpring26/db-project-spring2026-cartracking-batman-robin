class LocationPingDAO:
    def __init__(self, conn):
        self.conn = conn

    def vehicle_exists(self, vehicle_id: int) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM public.vehicle WHERE vehicle_id = %s;",
                (vehicle_id,)
            )
            return cursor.fetchone() is not None

    def create_location_ping(self, data: dict):
        lon, lat = data["geom"]["coordinates"]

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.location_ping (
                    vehicle_id,
                    ts,
                    geom,
                    speed_kph,
                    heading_deg
                )
                VALUES (
                    %s,
                    %s,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    %s,
                    %s
                )
                RETURNING
                    ping_id,
                    vehicle_id,
                    ts,
                    ST_AsGeoJSON(geom)::json AS geom,
                    speed_kph,
                    heading_deg;
                """,
                (
                    data["vehicle_id"],
                    data["ts"],
                    lon,
                    lat,
                    data.get("speed_kph"),
                    data.get("heading_deg"),
                )
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_location_pings(self, limit: int, offset: int, vehicle_id=None, from_ts=None, to_ts=None):
        query = """
            SELECT
                ping_id,
                vehicle_id,
                ts,
                ST_AsGeoJSON(geom)::json AS geom,
                speed_kph,
                heading_deg
            FROM public.location_ping
            WHERE 1=1
        """
        params = []

        if vehicle_id is not None:
            query += " AND vehicle_id = %s"
            params.append(vehicle_id)

        if from_ts is not None:
            query += " AND ts >= %s"
            params.append(from_ts)

        if to_ts is not None:
            query += " AND ts <= %s"
            params.append(to_ts)

        query += " ORDER BY ping_id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = "SELECT COUNT(*) AS total FROM public.location_ping WHERE 1=1"
            count_params = []

            if vehicle_id is not None:
                count_query += " AND vehicle_id = %s"
                count_params.append(vehicle_id)

            if from_ts is not None:
                count_query += " AND ts >= %s"
                count_params.append(from_ts)

            if to_ts is not None:
                count_query += " AND ts <= %s"
                count_params.append(to_ts)

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }

    def get_location_ping_by_id(self, ping_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    ping_id,
                    vehicle_id,
                    ts,
                    ST_AsGeoJSON(geom)::json AS geom,
                    speed_kph,
                    heading_deg
                FROM public.location_ping
                WHERE ping_id = %s;
                """,
                (ping_id,)
            )
            return cursor.fetchone()

    def update_location_ping(self, ping_id: int, data: dict):
        fields = []
        values = []

        for key, value in data.items():
            if key == "geom":
                lon, lat = value["coordinates"]
                fields.append("geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326)")
                values.extend([lon, lat])
            else:
                fields.append(f"{key} = %s")
                values.append(value)

        values.append(ping_id)

        query = f"""
            UPDATE public.location_ping
            SET {", ".join(fields)}
            WHERE ping_id = %s
            RETURNING
                ping_id,
                vehicle_id,
                ts,
                ST_AsGeoJSON(geom)::json AS geom,
                speed_kph,
                heading_deg;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def delete_location_ping(self, ping_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM public.location_ping WHERE ping_id = %s RETURNING ping_id;",
                (ping_id,)
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_vehicle_pings(self, vehicle_id: int, limit: int, offset: int, from_ts=None, to_ts=None):
        query = """
            SELECT
                ping_id,
                ts,
                ST_AsGeoJSON(geom)::json AS geom,
                speed_kph,
                heading_deg
            FROM public.location_ping
            WHERE vehicle_id = %s
        """
        params = [vehicle_id]

        if from_ts is not None:
            query += " AND ts >= %s"
            params.append(from_ts)

        if to_ts is not None:
            query += " AND ts <= %s"
            params.append(to_ts)

        query += " ORDER BY ts DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = "SELECT COUNT(*) AS total FROM public.location_ping WHERE vehicle_id = %s"
            count_params = [vehicle_id]

            if from_ts is not None:
                count_query += " AND ts >= %s"
                count_params.append(from_ts)

            if to_ts is not None:
                count_query += " AND ts <= %s"
                count_params.append(to_ts)

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "vehicle_id": vehicle_id,
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }