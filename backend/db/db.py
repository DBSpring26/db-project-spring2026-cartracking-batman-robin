import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(
        host="dpg-d6ovsu15pdvs739ofrn0-a.virginia-postgres.render.com",
        port=5432,
        dbname="declass",
        user="alexisagosto",
        password="ehx0AjqfLrNdUErWtDRLgimnorzscTDd",
        cursor_factory=RealDictCursor
    )
