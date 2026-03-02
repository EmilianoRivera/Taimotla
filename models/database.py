import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    return psycopg2.connect(
        dbname="nna_v2", 
        user="postgres",   
        password="4skay$@",    # ¡Pon tu contraseña real aquí!
        host="localhost",
        port="5432"
    )