import psycopg2


def get_connection():
    conn = psycopg2.connect(
        host="dpg-d6ovsu15pdvs739ofrn0-a.virginia-postgres.render.com",
        port=5432,
        dbname="declass",
        user="alexisagosto",
        password="ehx0AjqfLrNdUErWtDRLgimnorzscTDd"
    )
    return conn