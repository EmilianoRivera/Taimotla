import psycopg2
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()


def obtener_conexion():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port="5432",
    )


@contextmanager
def get_db_cursor(commit=False):
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        yield cur, conn
        if commit:
            conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
