from models.database import get_db_cursor
import psycopg2

def get_all_coordinators():
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute("""
                SELECT
                    c."CURP",
                    p.p_nombre || ' ' || COALESCE(p.s_nombre, '') || ' ' || p.p_apellido || ' ' || COALESCE(p.s_apellido, '') AS nombre
                FROM public.coordinador c
                JOIN public.persona p ON c."CURP" = p."CURP"
                JOIN public.personal per ON c."CURP" = per."CURP"
                JOIN public.estado_cuenta ec ON per.estado = ec.id_estado
                WHERE ec.estado = 'Activo'
            """)
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar coordinadores: {e}")
        return []

def get_available_staff():
    """
    Obtiene personal activo que no está en un equipo (fecha_fin IS NULL en composicion_equipo).
    Devuelve un diccionario agrupado por rol.
    """
    staff = {
        'abogado': [],
        'medico': [],
        'psicologo': [],
        'trabajadorsocial': []
    }
    try:
        with get_db_cursor() as (cur, conn):
            # Abogados
            cur.execute("""
                SELECT a."CURP", p.p_nombre || ' ' || p.p_apellido AS nombre, 'abogado' AS rol
                FROM public.abogado a
                JOIN public.persona p ON a."CURP" = p."CURP"
                JOIN public.personal per ON a."CURP" = per."CURP"
                JOIN public.estado_cuenta ec ON per.estado = ec.id_estado
                WHERE ec.estado = 'Activo' 
                  AND a."CURP" NOT IN (
                      SELECT curp_profesional FROM public.composicion_equipo WHERE fecha_fin IS NULL
                  )
            """)
            staff['abogado'] = cur.fetchall()

            # Médicos
            cur.execute("""
                SELECT m."CURP", p.p_nombre || ' ' || p.p_apellido AS nombre, 'medico' AS rol
                FROM public.medico m
                JOIN public.persona p ON m."CURP" = p."CURP"
                JOIN public.personal per ON m."CURP" = per."CURP"
                JOIN public.estado_cuenta ec ON per.estado = ec.id_estado
                WHERE ec.estado = 'Activo' 
                  AND m."CURP" NOT IN (
                      SELECT curp_profesional FROM public.composicion_equipo WHERE fecha_fin IS NULL
                  )
            """)
            staff['medico'] = cur.fetchall()

            # Psicólogos
            cur.execute("""
                SELECT ps."CURP", p.p_nombre || ' ' || p.p_apellido AS nombre, 'psicologo' AS rol
                FROM public.psicologo ps
                JOIN public.persona p ON ps."CURP" = p."CURP"
                JOIN public.personal per ON ps."CURP" = per."CURP"
                JOIN public.estado_cuenta ec ON per.estado = ec.id_estado
                WHERE ec.estado = 'Activo' 
                  AND ps."CURP" NOT IN (
                      SELECT curp_profesional FROM public.composicion_equipo WHERE fecha_fin IS NULL
                  )
            """)
            staff['psicologo'] = cur.fetchall()

            # Trabajadores Sociales
            cur.execute("""
                SELECT ts."CURP", p.p_nombre || ' ' || p.p_apellido AS nombre, 'trabajadorsocial' AS rol
                FROM public.trabajadorsocial ts
                JOIN public.persona p ON ts."CURP" = p."CURP"
                JOIN public.personal per ON ts."CURP" = per."CURP"
                JOIN public.estado_cuenta ec ON per.estado = ec.id_estado
                WHERE ec.estado = 'Activo' 
                  AND ts."CURP" NOT IN (
                      SELECT curp_profesional FROM public.composicion_equipo WHERE fecha_fin IS NULL
                  )
            """)
            staff['trabajadorsocial'] = cur.fetchall()
            
            return staff
    except psycopg2.Error as e:
        print(f"❌ Error al consultar personal disponible: {e}")
        return staff

def get_busy_staff():
    """
    Obtiene personal que está asignado actualmente a un equipo activo.
    """
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute("""
                SELECT p.p_nombre || ' ' || p.p_apellido AS nombre, 
                       eq.nombre_equipo
                FROM public.composicion_equipo ce
                JOIN public.persona p ON ce.curp_profesional = p."CURP"
                JOIN public.equipo eq ON ce.id_equipo = eq.id_equipo
                WHERE ce.fecha_fin IS NULL
            """)
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar personal ocupado: {e}")
        return []

def create_team(nombre_equipo, curp_coordinador, integrantes_curps):
    """
    Crea un equipo y su composición en una sola transacción.
    """
    try:
        with get_db_cursor(commit=True) as (cur, conn):
            # Obtener estado 'Activo' para el equipo
            cur.execute("SELECT id_estado_equipo FROM public.estado_equipo WHERE nombre_estado = 'Activo'")
            estado_row = cur.fetchone()
            if not estado_row:
                # Si no existe, lo insertamos
                cur.execute("INSERT INTO public.estado_equipo (nombre_estado) VALUES ('Activo') RETURNING id_estado_equipo")
                estado_row = cur.fetchone()
            id_estado_equipo = estado_row[0]

            # Insertar equipo
            cur.execute("""
                INSERT INTO public.equipo (nombre_equipo, curp_coordinador, id_estado_equipo)
                VALUES (%s, %s, %s)
                RETURNING id_equipo
            """, (nombre_equipo, curp_coordinador, id_estado_equipo))
            
            id_equipo = cur.fetchone()[0]

            # Insertar integrantes
            for curp in integrantes_curps:
                cur.execute("""
                    INSERT INTO public.composicion_equipo (id_equipo, curp_profesional)
                    VALUES (%s, %s)
                """, (id_equipo, curp))
            
            return True, "Equipo creado con éxito."
    except psycopg2.Error as e:
        print(f"❌ Error al crear equipo: {e}")
        return False, str(e)

def get_active_teams():
    try:
        with get_db_cursor() as (cur, conn):
            # Obtener estado Activo
            cur.execute("SELECT id_estado_equipo FROM public.estado_equipo WHERE nombre_estado = 'Activo'")
            estado_row = cur.fetchone()
            if not estado_row:
                return []
            id_estado_activo = estado_row[0]

            # Obtener equipos activos
            cur.execute("""
                SELECT e.id_equipo, e.nombre_equipo, e.curp_coordinador, 
                       p.p_nombre || ' ' || p.p_apellido AS nombre_coordinador
                FROM public.equipo e
                JOIN public.persona p ON e.curp_coordinador = p."CURP"
                WHERE e.id_estado_equipo = %s
                ORDER BY e.id_equipo DESC
            """, (id_estado_activo,))
            
            equipos_rows = cur.fetchall()
            equipos = []
            
            for eq in equipos_rows:
                id_equipo = eq[0]
                
                # Obtener miembros activos de este equipo
                # Necesitamos saber también el rol de cada integrante
                cur.execute("""
                    SELECT ce.curp_profesional, p.p_nombre || ' ' || p.p_apellido AS nombre,
                           CASE 
                               WHEN a."CURP" IS NOT NULL THEN 'abogado'
                               WHEN m."CURP" IS NOT NULL THEN 'medico'
                               WHEN ps."CURP" IS NOT NULL THEN 'psicologo'
                               WHEN ts."CURP" IS NOT NULL THEN 'trabajador social'
                               ELSE 'desconocido'
                           END AS rol
                    FROM public.composicion_equipo ce
                    JOIN public.persona p ON ce.curp_profesional = p."CURP"
                    LEFT JOIN public.abogado a ON ce.curp_profesional = a."CURP"
                    LEFT JOIN public.medico m ON ce.curp_profesional = m."CURP"
                    LEFT JOIN public.psicologo ps ON ce.curp_profesional = ps."CURP"
                    LEFT JOIN public.trabajadorsocial ts ON ce.curp_profesional = ts."CURP"
                    WHERE ce.id_equipo = %s AND ce.fecha_fin IS NULL
                """, (id_equipo,))
                
                miembros = cur.fetchall()
                
                equipos.append({
                    'id_equipo': eq[0],
                    'nombre_equipo': eq[1],
                    'curp_coordinador': eq[2],
                    'nombre_coordinador': eq[3],
                    'miembros': [{'curp': m[0], 'nombre': m[1], 'rol': m[2]} for m in miembros]
                })
            
            return equipos
    except psycopg2.Error as e:
        print(f"❌ Error al consultar equipos activos: {e}")
        return []

def add_member_to_team(id_equipo, curp_miembro):
    try:
        with get_db_cursor(commit=True) as (cur, conn):
            cur.execute("""
                INSERT INTO public.composicion_equipo (id_equipo, curp_profesional)
                VALUES (%s, %s)
            """, (id_equipo, curp_miembro))
            return True, "Miembro añadido exitosamente."
    except psycopg2.Error as e:
        print(f"❌ Error al añadir miembro: {e}")
        return False, str(e)

def remove_member_from_team(id_equipo, curp_miembro):
    try:
        with get_db_cursor(commit=True) as (cur, conn):
            cur.execute("""
                UPDATE public.composicion_equipo
                SET fecha_fin = CURRENT_DATE
                WHERE id_equipo = %s AND curp_profesional = %s AND fecha_fin IS NULL
            """, (id_equipo, curp_miembro))
            return True, "Miembro eliminado del equipo."
    except psycopg2.Error as e:
        print(f"❌ Error al eliminar miembro: {e}")
        return False, str(e)

def update_team_coordinator(id_equipo, curp_coordinador):
    try:
        with get_db_cursor(commit=True) as (cur, conn):
            cur.execute("""
                UPDATE public.equipo
                SET curp_coordinador = %s
                WHERE id_equipo = %s
            """, (curp_coordinador, id_equipo))
            return True, "Coordinador actualizado."
    except psycopg2.Error as e:
        print(f"❌ Error al actualizar coordinador: {e}")
        return False, str(e)

def delete_team(id_equipo):
    try:
        with get_db_cursor(commit=True) as (cur, conn):
            # Obtener o crear estado 'Inactivo' para equipo
            cur.execute("SELECT id_estado_equipo FROM public.estado_equipo WHERE nombre_estado = 'Inactivo'")
            estado_row = cur.fetchone()
            if not estado_row:
                cur.execute("INSERT INTO public.estado_equipo (nombre_estado) VALUES ('Inactivo') RETURNING id_estado_equipo")
                estado_row = cur.fetchone()
            id_estado_inactivo = estado_row[0]

            # Inactivar el equipo
            cur.execute("""
                UPDATE public.equipo
                SET id_estado_equipo = %s
                WHERE id_equipo = %s
            """, (id_estado_inactivo, id_equipo))

            # Cerrar las fechas de los integrantes activos
            cur.execute("""
                UPDATE public.composicion_equipo
                SET fecha_fin = CURRENT_DATE
                WHERE id_equipo = %s AND fecha_fin IS NULL
            """, (id_equipo,))
            
            return True, "Equipo eliminado correctamente."
    except psycopg2.Error as e:
        print(f"❌ Error al eliminar equipo: {e}")
        return False, str(e)
