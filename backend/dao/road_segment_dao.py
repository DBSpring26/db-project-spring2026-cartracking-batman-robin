class RoadSegmentDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_road_segment(self, data: dict):
        coords = data["geom"]["coordinates"]
        linestring = ", ".join([f"{lon} {lat}" for lon, lat in coords])
        wkt = f"LINESTRING({linestring})"

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.road_segment (
                    name,
                    speed_limit_kph,
                    geom,
                    created_at,
                    is_oneway,
                    direction
                )
                VALUES (
                    %s,
                    %s,
                    ST_GeomFromText(%s, 4326),
                    NOW(),
                    %s,
                    %s
                )
                RETURNING
                    road_id,
                    name,
                    speed_limit_kph,
                    ST_AsGeoJSON(geom)::json AS geom,
                    created_at,
                    is_oneway,
                    direction;
                """,
                (
                    data["name"],
                    data["speed_limit_kph"],
                    wkt,
                    data["is_oneway"],
                    data["direction"],
                )
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_road_segments(self, limit: int, offset: int, is_oneway=None, direction=None):
        query = """
            SELECT
                road_id,
                name,
                speed_limit_kph,
                ST_AsGeoJSON(geom)::json AS geom,
                created_at,
                is_oneway,
                direction
            FROM public.road_segment
            WHERE 1=1
        """
        params = []

        if is_oneway is not None:
            query += " AND is_oneway = %s"
            params.append(is_oneway)

        if direction is not None:
            query += " AND LOWER(direction) = LOWER(%s)"
            params.append(direction)

        query += " ORDER BY road_id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = "SELECT COUNT(*) AS total FROM public.road_segment WHERE 1=1"
            count_params = []

            if is_oneway is not None:
                count_query += " AND is_oneway = %s"
                count_params.append(is_oneway)

            if direction is not None:
                count_query += " AND LOWER(direction) = LOWER(%s)"
                count_params.append(direction)

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }

    def get_road_segment_by_id(self, road_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    road_id,
                    name,
                    speed_limit_kph,
                    ST_AsGeoJSON(geom)::json AS geom,
                    created_at,
                    is_oneway,
                    direction
                FROM public.road_segment
                WHERE road_id = %s;
                """,
                (road_id,)
            )
            return cursor.fetchone()

    def update_road_segment(self, road_id: int, data: dict):
        fields = []
        values = []

        for key, value in data.items():
            if key == "geom":
                coords = value["coordinates"]
                linestring = ", ".join([f"{lon} {lat}" for lon, lat in coords])
                wkt = f"LINESTRING({linestring})"
                fields.append("geom = ST_GeomFromText(%s, 4326)")
                values.append(wkt)
            else:
                fields.append(f"{key} = %s")
                values.append(value)

        values.append(road_id)

        query = f"""
            UPDATE public.road_segment
            SET {", ".join(fields)}
            WHERE road_id = %s
            RETURNING
                road_id,
                name,
                speed_limit_kph,
                ST_AsGeoJSON(geom)::json AS geom,
                created_at,
                is_oneway,
                direction;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def delete_road_segment(self, road_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM public.road_segment WHERE road_id = %s RETURNING road_id;",
                (road_id,)
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row