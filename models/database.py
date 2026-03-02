import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
def obtener_conexion():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'), 
        user=os.getenv('DB_USER'),   
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port="5432"
    )
