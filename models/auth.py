from models.database import obtener_conexion
import psycopg2


def verify_director(email):
    """
    Devuelve (CURP, p_nombre, contrasena, estado) si el correo
    pertenece a un director activo, o None si no existe.
    """
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query = """
                SELECT p."CURP",
                       p.p_nombre,
                       pers.contrasena,
                       pers.estado
                FROM   public.correos      c
                JOIN   public.persona      p    ON c.id_correo = p.id_correo
                JOIN   public.personal     pers ON p."CURP"    = pers."CURP"
                JOIN   public.director     d    ON p."CURP"    = d."CURP"
                WHERE  c.correo = %s
            """
            cur.execute(query, (email,))
            return cur.fetchone()
    except psycopg2.Error as e:
        print(f"[auth] Error en verify_director: {e}")
        return None
    finally:
        conn.close()


def verify_coordinador(email):
    """
    Devuelve (CURP, p_nombre, contrasena, estado) si el correo
    pertenece a un coordinador activo, o None si no existe.
    """
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query = """
                SELECT p."CURP",
                       p.p_nombre,
                       pers.contrasena,
                       pers.estado
                FROM   public.correos      c
                JOIN   public.persona      p    ON c.id_correo = p.id_correo
                JOIN   public.personal     pers ON p."CURP"    = pers."CURP"
                JOIN   public.coordinador  co   ON p."CURP"    = co."CURP"
                WHERE  c.correo = %s
            """
            cur.execute(query, (email,))
            return cur.fetchone()
    except psycopg2.Error as e:
        print(f"[auth] Error en verify_coordinador: {e}")
        return None
    finally:
        conn.close()