from models.database import obtener_conexion
from werkzeug.security import generate_password_hash
import psycopg2


def consult_coordinador(curp):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query_coordinador = """
                SELECT 
                    a."CURP", 
                    p.p_nombre || ' ' || p.p_apellido as nombre, 
                    a.estado,
                    'Coordinador' as rol
                FROM public.coordinador a 
                JOIN public.persona p ON p."CURP" = a."CURP"
                WHERE a."CURP" = %s; 
            """
            
            cur.execute(query_coordinador, (curp,))
            
            datos = cur.fetchall() 
            return datos
    except psycopg2.Error as e:
        print(f"❌ Error al consultar coordinador: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()
