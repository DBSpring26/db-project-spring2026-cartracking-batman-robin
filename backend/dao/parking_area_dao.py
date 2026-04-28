class ParkingAreaDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_parking_area(self, data):
        ring = data["geom"]["coordinates"][0]
        polygon = ", ".join([f"{lon} {lat}" for lon, lat in ring])
        wkt = f"POLYGON(({polygon}))"

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.parking_area (
                    name,
                    capacity,
                    geom,
                    created_at
                )
                VALUES (
                    %s,
                    %s,
                    ST_GeomFromText(%s, 4326),
                    NOW()
                )
                RETURNING
                    parking_area_id,
                    name,
                    capacity,
                    ST_AsGeoJSON(geom)::json as geom,
                    created_at;
                """,
                (
                    data["name"],
                    data["capacity"],
                    wkt
                )
            )

            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_parking_areas(self, limit, offset, name=None, capacity=None, bbox=None):
        query = """
            SELECT
                parking_area_id,
                name,
                capacity,
                ST_AsGeoJSON(geom)::json as geom,
                created_at
            FROM public.parking_area
            WHERE 1=1
        """

        params = []

        if name is not None:
            query += " AND name = %s"
            params.append(name)

        if capacity is not None:
            query += " AND capacity = %s"
            params.append(capacity)

        if bbox is not None:
            min_lon, min_lat, max_lon, max_lat = bbox

            query += """
                AND ST_Intersects(
                    geom,
                    ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                )
            """

            params.extend([min_lon, min_lat, max_lon, max_lat])

        query += """
            ORDER BY parking_area_id
            LIMIT %s OFFSET %s;
        """

        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = """
                SELECT COUNT(*) as total
                FROM public.parking_area
                WHERE 1=1
            """

            count_params = []

            if name is not None:
                count_query += " AND name = %s"
                count_params.append(name)

            if capacity is not None:
                count_query += " AND capacity = %s"
                count_params.append(capacity)

            if bbox is not None:
                min_lon, min_lat, max_lon, max_lat = bbox

                count_query += """
                    AND ST_Intersects(
                        geom,
                        ST_MakeEnvelope(%s, %s, %s, %s, 4326)
                    )
                """

                count_params.extend([min_lon, min_lat, max_lon, max_lat])

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

            return {
                "items": items,
                "limit": limit,
                "offset": offset,
                "count": count
            }

    def get_parking_area_by_id(self, parking_area_id):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    parking_area_id,
                    name,
                    capacity,
                    ST_AsGeoJSON(geom)::json as geom,
                    created_at
                FROM public.parking_area
                WHERE parking_area_id = %s;
                """,
                (parking_area_id,)
            )

            return cursor.fetchone()

    def update_parking_area(self, parking_area_id, data):
        fields = []
        values = []

        for key, value in data.items():
            if key == "geom":
                ring = value["coordinates"][0]
                polygon = ", ".join([f"{lon} {lat}" for lon, lat in ring])
                wkt = f"POLYGON(({polygon}))"

                fields.append("geom = ST_GeomFromText(%s, 4326)")
                values.append(wkt)

            else:
                fields.append(f"{key} = %s")
                values.append(value)

        values.append(parking_area_id)

        query = f"""
            UPDATE public.parking_area
            SET {", ".join(fields)}
            WHERE parking_area_id = %s
            RETURNING
                parking_area_id,
                name,
                capacity,
                ST_AsGeoJSON(geom)::json as geom,
                created_at;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def delete_parking_area(self, parking_area_id):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM public.parking_area
                WHERE parking_area_id = %s
                RETURNING parking_area_id;
                """,
                (parking_area_id,)
            )

            row = cursor.fetchone()
            self.conn.commit()
            return row