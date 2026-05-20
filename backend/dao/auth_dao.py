class AuthDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_user(self, username, password):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.app_user (username, password)
                VALUES (%s, %s)
                RETURNING user_id, username;
                """,
                (username, password)
            )
            row = cursor.fetchone()
            self.conn.commit()
            return row

    def get_user_by_username(self, username):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id, username, password
                FROM public.app_user
                WHERE username = %s;
                """,
                (username,)
            )
            return cursor.fetchone()