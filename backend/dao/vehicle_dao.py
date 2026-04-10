from typing import Optional


class VehicleDAO:
    def __init__(self, conn):
        self.conn = conn

    def vehicle_type_exists(self, vehicle_type_id: int) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM public.vehicle_type WHERE id = %s;",
                (vehicle_type_id,)
            )
            return cursor.fetchone() is not None

    def vehicle_status_exists(self, vehicle_status_id: int) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM public.vehicle_status WHERE vehicle_status_id = %s;",
                (vehicle_status_id,)
            )
            return cursor.fetchone() is not None

    def plate_number_exists(self, plate_number: str, exclude_vehicle_id: Optional[int] = None) -> bool:
        with self.conn.cursor() as cursor:
            if exclude_vehicle_id is None:
                cursor.execute(
                    "SELECT 1 FROM public.vehicle WHERE plate_number = %s;",
                    (plate_number,)
                )
            else:
                cursor.execute(
                    """
                    SELECT 1
                    FROM public.vehicle
                    WHERE plate_number = %s AND vehicle_id <> %s;
                    """,
                    (plate_number, exclude_vehicle_id)
                )
            return cursor.fetchone() is not None

    def create_vehicle(self, data: dict):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.vehicle (
                    vehicle_type_id,
                    vehicle_status_id,
                    plate_number,
                    make,
                    model,
                    year,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                RETURNING vehicle_id, vehicle_type_id, vehicle_status_id,
                          plate_number, make, model, year, created_at;
                """,
                (
                    data["vehicle_type_id"],
                    data["vehicle_status_id"],
                    data["plate_number"],
                    data.get("make"),
                    data.get("model"),
                    data.get("year"),
                )
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_vehicles(self, limit: int, offset: int, status=None, plate_number=None):
        query = """
            SELECT v.vehicle_id, v.plate_number, v.make, v.model, v.year,
                   v.vehicle_type_id, v.vehicle_status_id, v.created_at
            FROM public.vehicle v
            LEFT JOIN public.vehicle_status vs
              ON v.vehicle_status_id = vs.vehicle_status_id
            WHERE 1=1
        """
        params = []

        if status is not None:
            if str(status).isdigit():
                query += " AND v.vehicle_status_id = %s"
                params.append(int(status))
            else:
                query += " AND LOWER(vs.name) = LOWER(%s)"
                params.append(status)

        if plate_number is not None:
            query += " AND v.plate_number ILIKE %s"
            params.append(f"%{plate_number}%")

        query += " ORDER BY v.vehicle_id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

            count_query = """
                SELECT COUNT(*) AS total
                FROM public.vehicle v
                LEFT JOIN public.vehicle_status vs
                  ON v.vehicle_status_id = vs.vehicle_status_id
                WHERE 1=1
            """
            count_params = []

            if status is not None:
                if str(status).isdigit():
                    count_query += " AND v.vehicle_status_id = %s"
                    count_params.append(int(status))
                else:
                    count_query += " AND LOWER(vs.name) = LOWER(%s)"
                    count_params.append(status)

            if plate_number is not None:
                count_query += " AND v.plate_number ILIKE %s"
                count_params.append(f"%{plate_number}%")

            cursor.execute(count_query, tuple(count_params))
            count = cursor.fetchone()["total"]

        return {
            "items": items,
            "limit": limit,
            "offset": offset,
            "count": count
        }

    def get_vehicle_by_id(self, vehicle_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT vehicle_id, vehicle_type_id, vehicle_status_id,
                       plate_number, make, model, year, created_at
                FROM public.vehicle
                WHERE vehicle_id = %s;
                """,
                (vehicle_id,)
            )
            return cursor.fetchone()

    def update_vehicle(self, vehicle_id: int, data: dict):
        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(vehicle_id)

        query = f"""
            UPDATE public.vehicle
            SET {", ".join(fields)}
            WHERE vehicle_id = %s
            RETURNING vehicle_id, vehicle_type_id, vehicle_status_id,
                      plate_number, make, model, year, created_at;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def delete_vehicle(self, vehicle_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM public.vehicle WHERE vehicle_id = %s RETURNING vehicle_id;",
                (vehicle_id,)
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_vehicle_current_location(self, vehicle_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    v.vehicle_id,
                    v.plate_number,
                    vs.name AS status,
                    vk.name AS vehicle_kind,
                    ft.name AS fuel_type,
                    vt.emissions_rating,
                    lp.ts AS last_ts,
                    ST_AsGeoJSON(lp.geom)::json AS last_geom,
                    lp.speed_kph,
                    lp.heading_deg
                FROM public.vehicle v
                JOIN public.vehicle_status vs
                  ON v.vehicle_status_id = vs.vehicle_status_id
                JOIN public.vehicle_type vt
                  ON v.vehicle_type_id = vt.id
                JOIN public.vehicle_kind vk
                  ON vt.vehicle_kind_id = vk.vehicle_kind_id
                JOIN public.fuel_type ft
                  ON vt.fuel_type_id = ft.fuel_type_id
                JOIN public.location_ping lp
                  ON lp.vehicle_id = v.vehicle_id
                WHERE v.vehicle_id = %s
                ORDER BY lp.ts DESC
                LIMIT 1;
                """,
                (vehicle_id,)
            )
            return cursor.fetchone()