from models.database import obtener_conexion
from werkzeug.security import generate_password_hash
import psycopg2

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: obtener o crear registros de catálogo
# ─────────────────────────────────────────────────────────────────────────────

def _get_or_create_estado(cur, nombre_estado):
    cur.execute("SELECT id_estado FROM public.estados WHERE nombre_estado = %s", (nombre_estado,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO public.estados (nombre_estado) VALUES (%s) RETURNING id_estado", (nombre_estado,))
    return cur.fetchone()[0]

def _get_or_create_municipio(cur, nombre_municipio, id_estado):
    cur.execute("SELECT id_municipio FROM public.municipios WHERE nombre_municipio = %s AND id_estados_municipio = %s", (nombre_municipio, id_estado))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO public.municipios (nombre_municipio, id_estados_municipio) VALUES (%s, %s) RETURNING id_municipio", (nombre_municipio, id_estado))
    return cur.fetchone()[0]

def _get_or_create_cp(cur, codigo_postal):
    cur.execute("SELECT id_cp FROM public.codigo_postal WHERE codigo_postal = %s", (codigo_postal,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO public.codigo_postal (codigo_postal) VALUES (%s) RETURNING id_cp", (codigo_postal,))
    return cur.fetchone()[0]

def _get_or_create_colonia(cur, nombre_colonia, id_cp, id_municipio):
    cur.execute("SELECT id_colonia FROM public.colonia WHERE colonia = %s", (nombre_colonia,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO public.colonia (colonia, id_cp_colonia, id_municipios_colonia) VALUES (%s, %s, %s) RETURNING id_colonia",
        (nombre_colonia, id_cp, id_municipio)
    )
    return cur.fetchone()[0]

def _get_or_create_correo(cur, correo):
    cur.execute("SELECT id_correo FROM public.correos WHERE correo = %s", (correo,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO public.correos (correo) VALUES (%s) RETURNING id_correo", (correo,))
    return cur.fetchone()[0]

def _get_or_create_sexo(cur, sexo):
    cur.execute("SELECT id_sexo FROM public.sexo WHERE sexo = %s", (sexo,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO public.sexo (sexo) VALUES (%s) RETURNING id_sexo", (sexo,))
    return cur.fetchone()[0]

def _get_or_create_estado_cuenta(cur, estado='Activo'):
    cur.execute("SELECT id_estado FROM public.estado_cuenta WHERE estado = %s", (estado,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO public.estado_cuenta (estado) VALUES (%s) RETURNING id_estado", (estado,))
    return cur.fetchone()[0]


# ─────────────────────────────────────────────────────────────────────────────
# REGISTRAR USUARIO
# ─────────────────────────────────────────────────────────────────────────────

def user_register(data):
    password_hashed = generate_password_hash(data['contrasena'])

    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        # 1. Catálogos de ubicación
        id_estado_rep = _get_or_create_estado(cur, data['estado_rep'])
        id_municipio  = _get_or_create_municipio(cur, data['municipio'], id_estado_rep)
        id_cp         = _get_or_create_cp(cur, data['cp'])
        id_colonia    = _get_or_create_colonia(cur, data['colonia'], id_cp, id_municipio)

        # 2. Domicilio
        cur.execute("""
            INSERT INTO public.domicilio (num_ext, calle, id_colonia_domicilio)
            VALUES (%s, %s, %s) RETURNING id_domicilio
        """, (data['num_ext'], data['calle'], id_colonia))
        id_domicilio = cur.fetchone()[0]

        # 3. Correo
        id_correo = _get_or_create_correo(cur, data['correo'])

        # 4. Sexo
        id_sexo = _get_or_create_sexo(cur, data['sexo'])

        # 5. Persona
        cur.execute("""
            INSERT INTO public.persona (
                "CURP", "RFC", p_nombre, s_nombre, p_apellido, s_apellido,
                fecha_nacimiento, id_sexo_persona, id_domicilio_persona, id_correo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['curp'], data['rfc'],
            data['p_nombre'], data.get('s_nombre'),
            data['p_apellido'], data['s_apellido'],
            data['fecha_nacimiento'],
            id_sexo, id_domicilio, id_correo
        ))

        # 6. Estado de cuenta
        id_estado_cuenta = _get_or_create_estado_cuenta(cur, 'Activo')

        # 7. Personal
        cur.execute("""
            INSERT INTO public.personal ("CURP", fecha_alta, voluntario, contrasena, estado)
            VALUES (%s, CURRENT_DATE, False, %s, %s)
        """, (data['curp'], password_hashed, id_estado_cuenta))

        # 8. Tabla de rol específico
        rol = data['rol']
        if rol == 'trabajadorsocial':
            cur.execute("""
                INSERT INTO public.trabajadorsocial (cedula, "CURP")
                VALUES (%s, %s)
            """, (data['cedula'], data['curp']))

        elif rol == 'abogado':
            cur.execute("""
                INSERT INTO public.abogado (cedula, "CURP", especialidad)
                VALUES (%s, %s, %s)
            """, (data['cedula'], data['curp'], data.get('especialidad')))

        elif rol == 'medico':
            cur.execute("""
                INSERT INTO public.medico (cedula, "CURP", especialidad)
                VALUES (%s, %s, %s)
            """, (data['cedula'], data['curp'], data.get('especialidad')))

        elif rol == 'psicologo':
            cur.execute("""
                INSERT INTO public.psicologo (cedula, "CURP", enfoque_terapeutico)
                VALUES (%s, %s, %s)
            """, (data['cedula'], data['curp'], data.get('especialidad')))

        conn.commit()
        print(f"✅ Usuario {rol} registrado correctamente.")

    except psycopg2.Error as e:
        print(f"❌ Error al insertar: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# CONSULTAS (estado viene de personal.estado, no de la tabla de rol)
# ─────────────────────────────────────────────────────────────────────────────

def consult_lawyers():
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                a.cedula,
                a."CURP",
                p.p_nombre || ' ' || p.p_apellido AS nombre,
                a.especialidad,
                ec.estado,
                'Abogado' AS rol
            FROM  public.abogado    a
            JOIN  public.persona    p   ON p."CURP"  = a."CURP"
            JOIN  public.personal   per ON per."CURP" = a."CURP"
            JOIN  public.estado_cuenta ec ON ec.id_estado = per.estado
            WHERE ec.estado = 'Activo'
        """)
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al Consultar abogado: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_psico():
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                a.cedula,
                a."CURP",
                p.p_nombre || ' ' || p.p_apellido AS nombre,
                a.enfoque_terapeutico,
                ec.estado,
                'Psicólogo' AS rol
            FROM  public.psicologo  a
            JOIN  public.persona    p   ON p."CURP"  = a."CURP"
            JOIN  public.personal   per ON per."CURP" = a."CURP"
            JOIN  public.estado_cuenta ec ON ec.id_estado = per.estado
            WHERE ec.estado = 'Activo'
        """)
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar psicologo: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_social():
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                a.cedula,
                a."CURP",
                p.p_nombre || ' ' || p.p_apellido AS nombre,
                ec.estado,
                'Trabajador Social' AS rol
            FROM  public.trabajadorsocial a
            JOIN  public.persona          p   ON p."CURP"  = a."CURP"
            JOIN  public.personal         per ON per."CURP" = a."CURP"
            JOIN  public.estado_cuenta    ec  ON ec.id_estado = per.estado
            WHERE ec.estado = 'Activo'
        """)
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar trabajador social: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_medic():
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                a.cedula,
                a."CURP",
                p.p_nombre || ' ' || p.p_apellido AS nombre,
                a.especialidad,
                ec.estado,
                'Médico' AS rol
            FROM  public.medico     a
            JOIN  public.persona    p   ON p."CURP"  = a."CURP"
            JOIN  public.personal   per ON per."CURP" = a."CURP"
            JOIN  public.estado_cuenta ec ON ec.id_estado = per.estado
            WHERE ec.estado = 'Activo'
        """)
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar medico: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_director(curp):
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                p."CURP",
                per.fecha_alta,
                p.p_nombre || ' ' || p.p_apellido AS nombre,
                ec.estado,
                'Director' AS rol,
                p.p_nombre,
                p.s_nombre,
                p.p_apellido,
                p.s_apellido,
                p.fecha_nacimiento,
                sx.sexo,
                d.calle,
                d.num_ext,
                d.num_int,
                col.colonia,
                cp.codigo_postal,
                mun.nombre_municipio,
                est.nombre_estado,
                c.correo
            FROM  public.director      dir
            JOIN  public.persona       p   ON p."CURP"     = dir."CURP"
            JOIN  public.personal      per ON per."CURP"   = dir."CURP"
            JOIN  public.estado_cuenta ec  ON ec.id_estado = per.estado
            LEFT JOIN public.sexo      sx  ON sx.id_sexo   = p.id_sexo_persona
            LEFT JOIN public.domicilio d   ON d.id_domicilio = p.id_domicilio_persona
            LEFT JOIN public.colonia   col ON col.id_colonia = d.id_colonia_domicilio
            LEFT JOIN public.codigo_postal cp  ON cp.id_cp  = col.id_cp_colonia
            LEFT JOIN public.municipios    mun ON mun.id_municipio = col.id_municipios_colonia
            LEFT JOIN public.estados       est ON est.id_estado    = mun.id_estados_municipio
            LEFT JOIN public.correos       c   ON c.id_correo      = p.id_correo
            WHERE dir."CURP" = %s
        """, (curp,))
        return cur.fetchone()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar director: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()


def consult_unable_users():
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.p_nombre || ' ' || p.p_apellido, a."CURP", 'Abogado', ec.estado
            FROM public.abogado a
            JOIN public.persona p ON a."CURP" = p."CURP"
            JOIN public.personal per ON per."CURP" = a."CURP"
            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado
            WHERE ec.estado = 'Inactivo'

            UNION

            SELECT p.p_nombre || ' ' || p.p_apellido, m."CURP", 'Médico', ec.estado
            FROM public.medico m
            JOIN public.persona p ON m."CURP" = p."CURP"
            JOIN public.personal per ON per."CURP" = m."CURP"
            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado
            WHERE ec.estado = 'Inactivo'

            UNION

            SELECT p.p_nombre || ' ' || p.p_apellido, ts."CURP", 'Trabajador Social', ec.estado
            FROM public.trabajadorsocial ts
            JOIN public.persona p ON ts."CURP" = p."CURP"
            JOIN public.personal per ON per."CURP" = ts."CURP"
            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado
            WHERE ec.estado = 'Inactivo'

            UNION

            SELECT p.p_nombre || ' ' || p.p_apellido, ps."CURP", 'Psicólogo', ec.estado
            FROM public.psicologo ps
            JOIN public.persona p ON ps."CURP" = p."CURP"
            JOIN public.personal per ON per."CURP" = ps."CURP"
            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado
            WHERE ec.estado = 'Inactivo'
        """)
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar usuarios inhabilitados: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()


def desable_user(curp):
    """Cambia el estado de la cuenta a Inactivo en la tabla personal."""
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        # Obtener id del estado 'Inactivo'
        cur.execute("""
            INSERT INTO public.estado_cuenta (estado) VALUES ('Inactivo')
            ON CONFLICT DO NOTHING;
        """)
        cur.execute("SELECT id_estado FROM public.estado_cuenta WHERE estado = 'Inactivo'")
        id_inactivo = cur.fetchone()[0]

        cur.execute("""
            UPDATE public.personal SET estado = %s WHERE "CURP" = %s
        """, (id_inactivo, curp))

        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"❌ Error al inhabilitar al usuario: {e}")
        if conn: conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def able_user(curp):
    """Cambia el estado de la cuenta a Activo en la tabla personal."""
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT id_estado FROM public.estado_cuenta WHERE estado = 'Activo'")
        id_activo = cur.fetchone()[0]

        cur.execute("""
            UPDATE public.personal SET estado = %s WHERE "CURP" = %s
        """, (id_activo, curp))

        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"❌ Error al habilitar al usuario: {e}")
        if conn: conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def delete_user(curp):
    """
    Eliminar desde persona es suficiente: las tablas de rol y personal
    tienen ON DELETE CASCADE desde persona.
    """
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute('DELETE FROM public.persona WHERE "CURP" = %s', (curp,))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"❌ Error al eliminar: {e}")
        if conn: conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()


def search_one_user(curp):
    """Busca un usuario en todas las tablas de rol y devuelve un dict con sus datos."""
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        roles = {
            'abogado':         'abogado',
            'medico':          'medico',
            'psicologo':       'psicologo',
            'trabajadorsocial':'trabajadorsocial',
        }

        for tabla, rol in roles.items():
            cur.execute(f"""
                SELECT
                    p."CURP", p."RFC",
                    p.p_nombre, p.s_nombre, p.p_apellido, p.s_apellido,
                    sx.sexo,
                    p.fecha_nacimiento,
                    d.calle, d.num_ext, d.num_int,
                    col.colonia,
                    cp.codigo_postal,
                    mun.nombre_municipio,
                    est.nombre_estado,
                    c.correo
                FROM public.{tabla} a
                JOIN public.persona       p   ON p."CURP"       = a."CURP"
                LEFT JOIN public.sexo     sx  ON sx.id_sexo     = p.id_sexo_persona
                LEFT JOIN public.domicilio d  ON d.id_domicilio = p.id_domicilio_persona
                LEFT JOIN public.colonia  col ON col.id_colonia = d.id_colonia_domicilio
                LEFT JOIN public.codigo_postal cp  ON cp.id_cp  = col.id_cp_colonia
                LEFT JOIN public.municipios    mun ON mun.id_municipio = col.id_municipios_colonia
                LEFT JOIN public.estados       est ON est.id_estado    = mun.id_estados_municipio
                LEFT JOIN public.correos       c   ON c.id_correo      = p.id_correo
                WHERE a."CURP" = %s
            """, (curp,))
            res = cur.fetchone()
            if res:
                return {
                    'curp':            res[0],
                    'rfc':             res[1],
                    'p_nombre':        res[2],
                    's_nombre':        res[3],
                    'p_apellido':      res[4],
                    's_apellido':      res[5],
                    'sexo':            res[6],
                    'fecha_nacimiento':res[7],
                    'calle':           res[8],
                    'num_ext':         res[9],
                    'num_int':         res[10],
                    'colonia':         res[11],
                    'cp':              res[12],
                    'municipio':       res[13],
                    'estado_rep':      res[14],
                    'correo':          res[15],
                    'rol':             rol
                }
        return None

    except psycopg2.Error as e:
        print(f"❌ Error al buscar usuario: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()


def update_user(curp, data):
    """
    Actualiza los datos que pueden cambiar: correo, domicilio y nombre.
    Los datos de catálogo (colonia, municipio, cp, estado) se crean si no existen.
    """
    conn = None
    cur = None
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        # Actualizar ubicación solo si se enviaron todos los campos necesarios
        if all(data.get(k) for k in ('estado_rep', 'municipio', 'cp', 'colonia', 'calle')):
            id_estado_rep = _get_or_create_estado(cur, data['estado_rep'])
            id_municipio  = _get_or_create_municipio(cur, data['municipio'], id_estado_rep)
            id_cp         = _get_or_create_cp(cur, data['cp'])
            id_colonia    = _get_or_create_colonia(cur, data['colonia'], id_cp, id_municipio)

            # Obtener domicilio actual del usuario
            cur.execute("""
                SELECT id_domicilio_persona FROM public.persona WHERE "CURP" = %s
            """, (curp,))
            row = cur.fetchone()

            if row and row[0]:
                cur.execute("""
                    UPDATE public.domicilio
                    SET calle = %s, num_ext = %s, num_int = %s, id_colonia_domicilio = %s
                    WHERE id_domicilio = %s
                """, (data['calle'], data.get('num_ext'), data.get('num_int'), id_colonia, row[0]))
            else:
                cur.execute("""
                    INSERT INTO public.domicilio (calle, num_ext, num_int, id_colonia_domicilio)
                    VALUES (%s, %s, %s, %s) RETURNING id_domicilio
                """, (data['calle'], data.get('num_ext'), data.get('num_int'), id_colonia))
                id_dom_nuevo = cur.fetchone()[0]
                cur.execute("""
                    UPDATE public.persona SET id_domicilio_persona = %s WHERE "CURP" = %s
                """, (id_dom_nuevo, curp))

        # Actualizar correo
        if data.get('correo'):
            id_correo = _get_or_create_correo(cur, data['correo'])
            cur.execute("""
                UPDATE public.persona SET id_correo = %s WHERE "CURP" = %s
            """, (id_correo, curp))

        # Actualizar campos directos de persona
        cur.execute("""
            UPDATE public.persona
            SET "RFC"           = COALESCE(%s, "RFC"),
                p_nombre        = COALESCE(%s, p_nombre),
                s_nombre        = %s,
                p_apellido      = COALESCE(%s, p_apellido),
                s_apellido      = COALESCE(%s, s_apellido),
                fecha_nacimiento= COALESCE(%s, fecha_nacimiento)
            WHERE "CURP" = %s
        """, (
            data.get('rfc'),
            data.get('p_nombre'),
            data.get('s_nombre'),
            data.get('p_apellido'),
            data.get('s_apellido'),
            data.get('fecha_nacimiento') or None,
            curp
        ))

        # Actualizar sexo si se proporcionó
        if data.get('sexo'):
            id_sexo = _get_or_create_sexo(cur, data['sexo'])
            cur.execute("""
                UPDATE public.persona SET id_sexo_persona = %s WHERE "CURP" = %s
            """, (id_sexo, curp))

        conn.commit()
        return True

    except Exception as e:
        print(f"❌ Error al actualizar al usuario: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if cur: cur.close()
        if conn: conn.close()