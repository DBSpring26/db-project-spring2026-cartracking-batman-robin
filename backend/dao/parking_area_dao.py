class ParkingAreaDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_parking_area(self, data):

        ring = data["geom"]["coordinates"][0]

        polygon = ", ".join([f"{lon} {lat}" for lon, lat in ring])

        wkt = f"POLYGON(({polygon}))"

        with self.conn.cursor() as cursor:

            cursor.execute("""
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
            ))

            row = cursor.fetchone()

            self.conn.commit()

            return row


    def get_parking_areas(self, limit, offset):

        with self.conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    parking_area_id,
                    name,
                    capacity,
                    ST_AsGeoJSON(geom)::json as geom,
                    created_at
                FROM public.parking_area
                ORDER BY parking_area_id
                LIMIT %s OFFSET %s;
            """,
            (limit, offset))

            items = cursor.fetchall()

            cursor.execute("""
                SELECT COUNT(*) as total
                FROM public.parking_area;
            """)

            count = cursor.fetchone()["total"]

            return {
                "items": items,
                "limit": limit,
                "offset": offset,
                "count": count
            }


    def get_parking_area_by_id(self, parking_area_id):

        with self.conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    parking_area_id,
                    name,
                    capacity,
                    ST_AsGeoJSON(geom)::json as geom,
                    created_at
                FROM public.parking_area
                WHERE parking_area_id = %s;
            """,
            (parking_area_id,))

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

            cursor.execute("""
                DELETE FROM public.parking_area
                WHERE parking_area_id = %s
                RETURNING parking_area_id;
            """,
            (parking_area_id,))

            row = cursor.fetchone()
            self.conn.commit()

            return row