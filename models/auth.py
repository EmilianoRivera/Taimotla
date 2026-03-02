from models.database import obtener_conexion
import psycopg2

def verify_director(email):
    try: 
        conn =obtener_conexion()
        with conn.cursor() as cur:
            query = """SELECT d."CURP" as curp, d.contrasena as contrasena, p.p_nombre as Pnombre from public.persona p JOIN public.director d on p."CURP" = d."CURP" WHERE p.correo = %s"""
            
            cur.execute(query, (email,))

            return cur.fetchone()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Ocurrio un error: {e}")

