from models.database import obtener_conexion
from werkzeug.security import generate_password_hash
import psycopg2

def user_register(data):

    #Hash de contraseña
    password_plana = data['contrasena']
    password_hashed = generate_password_hash(password_plana)

    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            
            query_persona = """
                INSERT INTO public.persona (
                    "CURP", "RFC", p_nombre, s_nombre, p_apellido, s_apellido, sexo, fecha_nacimiento, calle, num_ext, colonia, cp, municipio, estado_rep, telefono, correo
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """

            insert_data = (
                    data['curp'], 
                    data['rfc'], 
                    data['p_nombre'], 
                    data['s_nombre'], 
                    data['p_apellido'], 
                    data['s_apellido'],
                    data['sexo'], 
                    data['fecha_nacimiento'], 
                    data['calle'], 
                    data['num_ext'], 
                    data['colonia'], 
                    data['cp'], 
                    data['municipio'], 
                    data['estado_rep'], 
                    data['telefono'], 
                    data['correo']
                    )
            
           
            if data['rol'] == 'trabajadorsocial':
                query_trabajadorsocial = """
                INSERT INTO public.trabajadorsocial (cedula, "CURP", contrasena, estado) VALUES (%s, %s, %s, %s)
                """
                insert_data_trabajadorsocial =(data['cedula'], data['curp'], password_hashed, 'Activo')

                cur.execute(query_persona, insert_data)
                cur.execute(query_trabajadorsocial,insert_data_trabajadorsocial )

                conn.commit()
                print("✅ Trabajador social insertado correctamente con contraseña hasheada.")
            elif data['rol'] == 'abogado' :
                query_abogado = """ 
                INSERT INTO public.abogado (cedula, "CURP", especialidad, contrasena, estado) VALUES (%s, %s, %s, %s, %s)    
                """

                insert_data_abogado = (data['cedula'], data['curp'], data['especialidad'], password_hashed, 'Activo')

                cur.execute(query_persona, insert_data)
                cur.execute(query_abogado, insert_data_abogado)

                conn.commit()
                print("✅ Abogado insertado correctamente con contraseña hasheada.")
            elif data['rol'] == 'medico' :
                query_medico = """ 
                INSERT INTO public.medico (cedula, "CURP", especialidad, contrasena, estado) VALUES (%s, %s, %s, %s, %s)    
                """

                insert_data_medico = (data['cedula'], data['curp'], data['especialidad'], password_hashed, 'Activo')

                cur.execute(query_persona, insert_data)
                cur.execute(query_medico, insert_data_medico)

                conn.commit()
                print("✅ Medico insertado correctamente con contraseña hasheada.")
            elif data['rol'] == 'psicologo' :
                query_psicologo = """ 
                INSERT INTO public.psicologo (cedula, "CURP", enfoque_terapeutico, contrasena, estado) VALUES (%s, %s, %s, %s, %s)    
                """

                insert_data_psicologo = (data['cedula'], data['curp'], data['especialidad'], password_hashed, 'Activo')

                cur.execute(query_persona, insert_data)
                cur.execute(query_psicologo, insert_data_psicologo)

                conn.commit()
                print("✅ Medico insertado correctamente con contraseña hasheada.")
    except psycopg2.Error as e:
        print(f"❌ Error al insertar: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_lawyers():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query_abogados = """
                SELECT 
                    a.cedula, 
                    a."CURP", 
                    p.p_nombre || ' ' || p.p_apellido as nombre, 
                    a.especialidad, 
                    a.estado,
                    'Abogado' as rol
                FROM public.abogado a 
                JOIN public.persona p ON p."CURP" = a."CURP";
            """
            
            # 2. Ejecutamos solo una consulta a la vez o usamos UNION
            cur.execute(query_abogados)
            
            # 3. USA fetchall() para traer a TODOS, no solo a uno
            datos = cur.fetchall() 
            return datos
    except psycopg2.Error as e:
        print(f"❌ Error al Consultar abogado: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()

def consult_psico():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query_psico = """
                SELECT 
                    a.cedula, 
                    a."CURP", 
                    p.p_nombre || ' ' || p.p_apellido as nombre, 
                    a.enfoque_terapeutico, 
                    a.estado,
                    'psicologo' as rol
                FROM public.psicologo a 
                JOIN public.persona p ON p."CURP" = a."CURP";
            """
            
            # 2. Ejecutamos solo una consulta a la vez o usamos UNION
            cur.execute(query_psico)
            
            # 3. USA fetchall() para traer a TODOS, no solo a uno
            datos = cur.fetchall() 
            return datos
    except psycopg2.Error as e:
        print(f"❌ Error al consultar psicologo: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_social():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query_social = """
                SELECT 
                    a.cedula, 
                    a."CURP", 
                    p.p_nombre || ' ' || p.p_apellido as nombre, 
                    a.estado,
                    'Trabajador Social' as rol
                FROM public.trabajadorsocial a 
                JOIN public.persona p ON p."CURP" = a."CURP";
            """
            
            cur.execute(query_social)
            
            datos = cur.fetchall() 
            return datos
    except psycopg2.Error as e:
        print(f"❌ Error al consultar trabajador social: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_medic():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query_medicos = """
                SELECT 
                    a.cedula, 
                    a."CURP", 
                    p.p_nombre || ' ' || p.p_apellido as nombre, 
                    a.especialidad, 
                    a.estado,
                    'medico' as rol
                FROM public.medico a 
                JOIN public.persona p ON p."CURP" = a."CURP";
            """
            
            cur.execute(query_medicos)
            
            datos = cur.fetchall() 
            return datos
    except psycopg2.Error as e:
        print(f"❌ Error al consultar medico: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()

def consult_director(curp):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query_director = """
                SELECT 
                    a."CURP", 
                    a.fecha_ingreso,
                    p.p_nombre || ' ' || p.p_apellido as nombre, 
                    a.estado,
                    'Director' as rol
                FROM public.director a 
                JOIN public.persona p ON p."CURP" = a."CURP"
                WHERE a."CURP" = %s; 
            """
            
            cur.execute(query_director, (curp,))
            
            datos = cur.fetchall() 
            return datos
    except psycopg2.Error as e:
        print(f"❌ Error al consultar director: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def delete_user(curp):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            tablas_roles = ['psicologo', 'trabajadorsocial', 'abogado', 'medico']
            
            for tabla in tablas_roles:
                cur.execute(f'DELETE FROM public.{tabla} WHERE "CURP" = %s', (curp,))

            cur.execute('DELETE FROM public.persona WHERE "CURP" = %s', (curp,))
            
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Error al eliminar: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()

def desable_user(curp):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            tablas_roles = [ 'psicologo', 'trabajadorsocial', 'abogado', 'medico']
            
            for tabla in tablas_roles:
                cur.execute(f'UPDATE public.{tabla} SET estado = %s WHERE "CURP" = %s', ("Inactivo",curp,))

            
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Error al inhabilitar al usuario: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_unable_users():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query = """
                SELECT p.p_nombre || ' ' || p.p_apellido, a."CURP", 'Abogado', a.estado 
                FROM abogado a JOIN persona p ON a."CURP" = p."CURP" WHERE a.estado = 'Inactivo'
                UNION
                SELECT p.p_nombre || ' ' || p.p_apellido, m."CURP", 'Médico', m.estado 
                FROM medico m JOIN persona p ON m."CURP" = p."CURP" WHERE m.estado = 'Inactivo'
                UNION
                SELECT p.p_nombre || ' ' || p.p_apellido, ts."CURP", 'TrabajadorSocial', ts.estado
                FROM  trabajadorsocial ts JOIN  persona p ON ts."CURP" = p."CURP" WHERE ts.estado = 'Inactivo'
                UNION
                SELECT p.p_nombre || ' ' || p.p_apellido, ps."CURP", 'Psicólogo', ps.estado 
                FROM psicologo ps JOIN persona p ON ps."CURP" = p."CURP" WHERE ps.estado = 'Inactivo';
            """
            cur.execute(query)
            return cur.fetchall()
        
    except psycopg2.Error as e:
        print(f"❌ Error al inhabilitar al usuario: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def able_user(curp):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            tablas_roles = [ 'psicologo', 'trabajadorsocial', 'abogado', 'medico']
            
            for tabla in tablas_roles:
                cur.execute(f'UPDATE public.{tabla} SET estado = %s WHERE "CURP" = %s', ("Activo",curp,))

            
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Error al habilitar al usuario: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()   


def search_one_user(curp):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            tablas_roles = [ 'psicologo', 'trabajadorsocial', 'abogado', 'medico']
            for tabla in tablas_roles:
                query_get_user = f"""
                SELECT 
                    a."CURP" as curp,
                    p.p_nombre || ' ' || p.p_apellido as nombre_completo, 
                    p.telefono, 
                    p.calle,
                    p.correo

                FROM public.{tabla} a 
                JOIN public.persona p ON a."CURP" = p."CURP" 
                WHERE p."CURP" = %s
                """
                res = cur.execute(query_get_user, (curp,))
                res = cur.fetchone()
                if res:
                    return {
                        'curp': res[0],
                        'nombre': res[1],
                        'telefono': res[2],
                        'calle': res[3],
                        'correo': res[4],
                        'rol': tabla
                    }
            
            return None
            
    except psycopg2.Error as e:
        print(f"❌ Error al habilitar al usuario: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()  


def update_user(curp, data):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            query = """
                UPDATE public.persona 
                SET correo = %s, telefono = %s, calle = %s 
                WHERE "CURP" = %s
            """
            cur.execute(query, (
                data.get('correo'), 
                data.get('telefono'), 
                data.get('calle'), 
                curp
            ))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Error al actualizar al usuario: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()  