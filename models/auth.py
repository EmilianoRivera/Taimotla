from models.database import obtener_conexion
import psycopg2

def verify_director(email):
    try: 
        conn =obtener_conexion()
        with conn.cursor() as cur:
            query = """ SELECT p."CURP", p.p_nombre, pers.contrasena FROM  public.correos c 
                        JOIN public.persona p ON c.correo = p.id_correo 
                        JOIN public.personal pers ON p."CURP" = pers."CURP" 
                        WHERE c.correo = %s"""
            
            cur.execute(query, (email,))
            return cur.fetchone()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Ocurrio un error: {e}")

def verify_coordinador (email):
    try: 
        conn =obtener_conexion()
        with conn.cursor() as cur:
            query = """ SELECT p."CURP", p.p_nombre, pers.contrasena FROM  public.correos c 
                        JOIN public.persona p ON c.correo = p.id_correo 
                        JOIN public.personal pers ON p."CURP" = pers."CURP" 
                        WHERE c.correo = %s"""
            
            cur.execute(query, (email,))

            return cur.fetchone()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Ocurrio un error: {e}")

