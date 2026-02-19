import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    return psycopg2.connect(
        dbname="nna", # El nombre que pusiste en tu script
        user="postgres",           # Tu usuario de Postgres
        password="4skay$@",    # ¡Pon tu contraseña real aquí!
        host="localhost",
        port="5432"
    )