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

    def get_location_pings(
        self,
        limit: int,
        offset: int,
        vehicle_id=None,
        from_ts=None,
        to_ts=None,
        bbox=None
    ):
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

        if bbox is not None:
            min_lon, min_lat, max_lon, max_lat = bbox

            query += """
                AND ST_Intersects(
                    geom,
                    ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                )
            """

            params.extend([
                min_lon,
                min_lat,
                max_lon,
                max_lat
            ])

        query += """
            ORDER BY ping_id
            LIMIT %s OFFSET %s
        """

        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = """
                SELECT COUNT(*) AS total
                FROM public.location_ping
                WHERE 1=1
            """

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

            if bbox is not None:
                min_lon, min_lat, max_lon, max_lat = bbox

                count_query += """
                    AND ST_Intersects(
                        geom,
                        ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                    )
                """

                count_params.extend([
                    min_lon,
                    min_lat,
                    max_lon,
                    max_lat
                ])

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

                fields.append(
                    "geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326)"
                )

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
                """
                DELETE FROM public.location_ping
                WHERE ping_id = %s
                RETURNING ping_id;
                """,
                (ping_id,)
            )

            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_vehicle_pings(
        self,
        vehicle_id: int,
        limit: int,
        offset: int,
        from_ts=None,
        to_ts=None,
        bbox=None
    ):
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

        if bbox is not None:
            min_lon, min_lat, max_lon, max_lat = bbox

            query += """
                AND ST_Intersects(
                    geom,
                    ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                )
            """

            params.extend([
                min_lon,
                min_lat,
                max_lon,
                max_lat
            ])

        query += """
            ORDER BY ts DESC
            LIMIT %s OFFSET %s
        """

        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = """
                SELECT COUNT(*) AS total
                FROM public.location_ping
                WHERE vehicle_id = %s
            """

            count_params = [vehicle_id]

            if from_ts is not None:
                count_query += " AND ts >= %s"
                count_params.append(from_ts)

            if to_ts is not None:
                count_query += " AND ts <= %s"
                count_params.append(to_ts)

            if bbox is not None:
                min_lon, min_lat, max_lon, max_lat = bbox

                count_query += """
                    AND ST_Intersects(
                        geom,
                        ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                    )
                """

                count_params.extend([
                    min_lon,
                    min_lat,
                    max_lon,
                    max_lat
                ])

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "vehicle_id": vehicle_id,
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }

    # ---------------- FASE 3 ----------------

    def get_latest_vehicle_pings(
        self,
        limit: int,
        offset: int,
        bbox=None
    ):
        query = """
            SELECT DISTINCT ON (vehicle_id)
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

        if bbox is not None:
            min_lon, min_lat, max_lon, max_lat = bbox

            query += """
                AND ST_Intersects(
                    geom,
                    ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                )
            """

            params.extend([
                min_lon,
                min_lat,
                max_lon,
                max_lat
            ])

        query += """
            ORDER BY vehicle_id, ts DESC
            LIMIT %s OFFSET %s
        """

        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = """
                SELECT COUNT(DISTINCT vehicle_id) AS total
                FROM public.location_ping
                WHERE 1=1
            """

            count_params = []

            if bbox is not None:
                min_lon, min_lat, max_lon, max_lat = bbox

                count_query += """
                    AND ST_Intersects(
                        geom,
                        ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                    )
                """

                count_params.extend([
                    min_lon,
                    min_lat,
                    max_lon,
                    max_lat
                ])

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }

    def get_breadcrumb(
        self,
        vehicle_id: int,
        start_ts: str,
        end_ts: str
    ):
        query = """
            SELECT
                t.trip_id,
                lp.ping_id,
                lp.vehicle_id,
                lp.ts,
                ST_AsGeoJSON(lp.geom)::json AS geom,
                lp.speed_kph,
                lp.heading_deg
            FROM public.location_ping lp
            LEFT JOIN public.trip t
              ON t.vehicle_id = lp.vehicle_id
             AND lp.ts BETWEEN t.start_ts AND t.end_ts
            WHERE lp.vehicle_id = %s
              AND lp.ts >= %s
              AND lp.ts <= %s
            ORDER BY lp.ts ASC
        """

        with self.conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    vehicle_id,
                    start_ts,
                    end_ts
                )
            )

            rows = cursor.fetchall()

        trip_ids = []

        for row in rows:
            if row["trip_id"] is not None and row["trip_id"] not in trip_ids:
                trip_ids.append(row["trip_id"])

        return {
            "vehicle_id": vehicle_id,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "trip_ids": trip_ids,
            "items": rows,
            "count": len(rows)
        }

    def get_pings_per_day(self):
        query = """
            SELECT
                DATE(ts) AS day,
                COUNT(*) AS total_pings
            FROM public.location_ping
            GROUP BY DATE(ts)
            ORDER BY day ASC
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            items = cursor.fetchall()

        return {
            "items": items,
            "count": len(items)
        }