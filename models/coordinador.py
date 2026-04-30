from models.database import get_db_cursor
from werkzeug.security import generate_password_hash
import psycopg2


def consult_coordinador(curp):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query_coordinador = '\n                SELECT \n                    a."CURP", \n                    p.p_nombre || \' \' || p.p_apellido as nombre, \n                    a.estado,\n                    \'Coordinador\' as rol\n                FROM public.coordinador a \n                JOIN public.persona p ON p."CURP" = a."CURP"\n                WHERE a."CURP" = %s; \n            '
            cur.execute(query_coordinador, (curp,))
            datos = cur.fetchall()
            return datos
    except psycopg2.Error as e:
        print(f"❌ Error al consultar coordinador: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
