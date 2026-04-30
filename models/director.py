from models.database import get_db_cursor
from werkzeug.security import generate_password_hash
import psycopg2


def _get_or_create_estado(cur, nombre_estado):
    cur.execute(
        "SELECT id_estado FROM public.estados WHERE nombre_estado = %s",
        (nombre_estado,),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO public.estados (nombre_estado) VALUES (%s) RETURNING id_estado",
        (nombre_estado,),
    )
    return cur.fetchone()[0]


def _get_or_create_municipio(cur, nombre_municipio, id_estado):
    cur.execute(
        "SELECT id_municipio FROM public.municipios WHERE nombre_municipio = %s AND id_estados_municipio = %s",
        (nombre_municipio, id_estado),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO public.municipios (nombre_municipio, id_estados_municipio) VALUES (%s, %s) RETURNING id_municipio",
        (nombre_municipio, id_estado),
    )
    return cur.fetchone()[0]


def _get_or_create_cp(cur, codigo_postal):
    cur.execute(
        "SELECT id_cp FROM public.codigo_postal WHERE codigo_postal = %s",
        (codigo_postal,),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO public.codigo_postal (codigo_postal) VALUES (%s) RETURNING id_cp",
        (codigo_postal,),
    )
    return cur.fetchone()[0]


def _get_or_create_colonia(cur, nombre_colonia, id_cp, id_municipio):
    cur.execute(
        "SELECT id_colonia FROM public.colonia WHERE colonia = %s", (nombre_colonia,)
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO public.colonia (colonia, id_cp_colonia, id_municipios_colonia) VALUES (%s, %s, %s) RETURNING id_colonia",
        (nombre_colonia, id_cp, id_municipio),
    )
    return cur.fetchone()[0]


def _get_or_create_correo(cur, correo):
    cur.execute("SELECT id_correo FROM public.correos WHERE correo = %s", (correo,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO public.correos (correo) VALUES (%s) RETURNING id_correo", (correo,)
    )
    return cur.fetchone()[0]


def _get_or_create_sexo(cur, sexo):
    cur.execute("SELECT id_sexo FROM public.sexo WHERE sexo = %s", (sexo,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO public.sexo (sexo) VALUES (%s) RETURNING id_sexo", (sexo,))
    return cur.fetchone()[0]


def _get_or_create_estado_cuenta(cur, estado="Activo"):
    cur.execute(
        "SELECT id_estado FROM public.estado_cuenta WHERE estado = %s", (estado,)
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO public.estado_cuenta (estado) VALUES (%s) RETURNING id_estado",
        (estado,),
    )
    return cur.fetchone()[0]


def user_register(data):
    password_hashed = generate_password_hash(data["contrasena"])
    try:
        with get_db_cursor() as (cur, conn):
            id_estado_rep = _get_or_create_estado(cur, data["estado_rep"])
            id_municipio = _get_or_create_municipio(
                cur, data["municipio"], id_estado_rep
            )
            id_cp = _get_or_create_cp(cur, data["cp"])
            id_colonia = _get_or_create_colonia(
                cur, data["colonia"], id_cp, id_municipio
            )
            cur.execute(
                "\n            INSERT INTO public.domicilio (num_ext, calle, id_colonia_domicilio)\n            VALUES (%s, %s, %s) RETURNING id_domicilio\n        ",
                (data["num_ext"], data["calle"], id_colonia),
            )
            id_domicilio = cur.fetchone()[0]
            id_correo = _get_or_create_correo(cur, data["correo"])
            id_sexo = _get_or_create_sexo(cur, data["sexo"])
            cur.execute(
                '\n            INSERT INTO public.persona (\n                "CURP", "RFC", p_nombre, s_nombre, p_apellido, s_apellido,\n                fecha_nacimiento, id_sexo_persona, id_domicilio_persona, id_correo\n            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)\n        ',
                (
                    data["curp"],
                    data["rfc"],
                    data["p_nombre"],
                    data.get("s_nombre"),
                    data["p_apellido"],
                    data["s_apellido"],
                    data["fecha_nacimiento"],
                    id_sexo,
                    id_domicilio,
                    id_correo,
                ),
            )
            id_estado_cuenta = _get_or_create_estado_cuenta(cur, "Activo")
            cur.execute(
                '\n            INSERT INTO public.personal ("CURP", fecha_alta, voluntario, contrasena, estado)\n            VALUES (%s, CURRENT_DATE, False, %s, %s)\n        ',
                (data["curp"], password_hashed, id_estado_cuenta),
            )
            rol = data["rol"]
            if rol == "trabajadorsocial":
                cur.execute(
                    '\n                INSERT INTO public.trabajadorsocial (cedula, "CURP")\n                VALUES (%s, %s)\n            ',
                    (data["cedula"], data["curp"]),
                )
            elif rol == "abogado":
                cur.execute(
                    '\n                INSERT INTO public.abogado (cedula, "CURP", especialidad)\n                VALUES (%s, %s, %s)\n            ',
                    (data["cedula"], data["curp"], data.get("especialidad")),
                )
            elif rol == "medico":
                cur.execute(
                    '\n                INSERT INTO public.medico (cedula, "CURP", especialidad)\n                VALUES (%s, %s, %s)\n            ',
                    (data["cedula"], data["curp"], data.get("especialidad")),
                )
            elif rol == "psicologo":
                cur.execute(
                    '\n                INSERT INTO public.psicologo (cedula, "CURP", enfoque_terapeutico)\n                VALUES (%s, %s, %s)\n            ',
                    (data["cedula"], data["curp"], data.get("especialidad")),
                )
            conn.commit()
            print(f"✅ Usuario {rol} registrado correctamente.")
    except psycopg2.Error as e:
        print(f"❌ Error al insertar: {e}")


def consult_lawyers():
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                '\n            SELECT\n                a.cedula,\n                a."CURP",\n                p.p_nombre || \' \' || p.p_apellido AS nombre,\n                a.especialidad,\n                ec.estado,\n                \'Abogado\' AS rol\n            FROM  public.abogado    a\n            JOIN  public.persona    p   ON p."CURP"  = a."CURP"\n            JOIN  public.personal   per ON per."CURP" = a."CURP"\n            JOIN  public.estado_cuenta ec ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Activo\'\n        '
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al Consultar abogado: {e}")


def consult_psico():
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                '\n            SELECT\n                a.cedula,\n                a."CURP",\n                p.p_nombre || \' \' || p.p_apellido AS nombre,\n                a.enfoque_terapeutico,\n                ec.estado,\n                \'Psicólogo\' AS rol\n            FROM  public.psicologo  a\n            JOIN  public.persona    p   ON p."CURP"  = a."CURP"\n            JOIN  public.personal   per ON per."CURP" = a."CURP"\n            JOIN  public.estado_cuenta ec ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Activo\'\n        '
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar psicologo: {e}")


def consult_social():
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                '\n            SELECT\n                a.cedula,\n                a."CURP",\n                p.p_nombre || \' \' || p.p_apellido AS nombre,\n                ec.estado,\n                \'Trabajador Social\' AS rol\n            FROM  public.trabajadorsocial a\n            JOIN  public.persona          p   ON p."CURP"  = a."CURP"\n            JOIN  public.personal         per ON per."CURP" = a."CURP"\n            JOIN  public.estado_cuenta    ec  ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Activo\'\n        '
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar trabajador social: {e}")


def consult_medic():
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                '\n            SELECT\n                a.cedula,\n                a."CURP",\n                p.p_nombre || \' \' || p.p_apellido AS nombre,\n                a.especialidad,\n                ec.estado,\n                \'Médico\' AS rol\n            FROM  public.medico     a\n            JOIN  public.persona    p   ON p."CURP"  = a."CURP"\n            JOIN  public.personal   per ON per."CURP" = a."CURP"\n            JOIN  public.estado_cuenta ec ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Activo\'\n        '
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar medico: {e}")


def consult_director(curp):
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                '\n            SELECT\n                p."CURP",\n                per.fecha_alta,\n                p.p_nombre || \' \' || p.p_apellido AS nombre,\n                ec.estado,\n                \'Director\' AS rol,\n                p.p_nombre,\n                p.s_nombre,\n                p.p_apellido,\n                p.s_apellido,\n                p.fecha_nacimiento,\n                sx.sexo,\n                d.calle,\n                d.num_ext,\n                d.num_int,\n                col.colonia,\n                cp.codigo_postal,\n                mun.nombre_municipio,\n                est.nombre_estado,\n                c.correo\n            FROM  public.director      dir\n            JOIN  public.persona       p   ON p."CURP"     = dir."CURP"\n            JOIN  public.personal      per ON per."CURP"   = dir."CURP"\n            JOIN  public.estado_cuenta ec  ON ec.id_estado = per.estado\n            LEFT JOIN public.sexo      sx  ON sx.id_sexo   = p.id_sexo_persona\n            LEFT JOIN public.domicilio d   ON d.id_domicilio = p.id_domicilio_persona\n            LEFT JOIN public.colonia   col ON col.id_colonia = d.id_colonia_domicilio\n            LEFT JOIN public.codigo_postal cp  ON cp.id_cp  = col.id_cp_colonia\n            LEFT JOIN public.municipios    mun ON mun.id_municipio = col.id_municipios_colonia\n            LEFT JOIN public.estados       est ON est.id_estado    = mun.id_estados_municipio\n            LEFT JOIN public.correos       c   ON c.id_correo      = p.id_correo\n            WHERE dir."CURP" = %s\n        ',
                (curp,),
            )
            return cur.fetchone()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar director: {e}")


def consult_unable_users():
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                '\n            SELECT p.p_nombre || \' \' || p.p_apellido, a."CURP", \'Abogado\', ec.estado\n            FROM public.abogado a\n            JOIN public.persona p ON a."CURP" = p."CURP"\n            JOIN public.personal per ON per."CURP" = a."CURP"\n            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Inactivo\'\n\n            UNION\n\n            SELECT p.p_nombre || \' \' || p.p_apellido, m."CURP", \'Médico\', ec.estado\n            FROM public.medico m\n            JOIN public.persona p ON m."CURP" = p."CURP"\n            JOIN public.personal per ON per."CURP" = m."CURP"\n            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Inactivo\'\n\n            UNION\n\n            SELECT p.p_nombre || \' \' || p.p_apellido, ts."CURP", \'Trabajador Social\', ec.estado\n            FROM public.trabajadorsocial ts\n            JOIN public.persona p ON ts."CURP" = p."CURP"\n            JOIN public.personal per ON per."CURP" = ts."CURP"\n            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Inactivo\'\n\n            UNION\n\n            SELECT p.p_nombre || \' \' || p.p_apellido, ps."CURP", \'Psicólogo\', ec.estado\n            FROM public.psicologo ps\n            JOIN public.persona p ON ps."CURP" = p."CURP"\n            JOIN public.personal per ON per."CURP" = ps."CURP"\n            JOIN public.estado_cuenta ec ON ec.id_estado = per.estado\n            WHERE ec.estado = \'Inactivo\'\n        '
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        print(f"❌ Error al consultar usuarios inhabilitados: {e}")


def desable_user(curp):
    "Cambia el estado de la cuenta a Inactivo en la tabla personal."
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                "\n            INSERT INTO public.estado_cuenta (estado) VALUES ('Inactivo')\n            ON CONFLICT DO NOTHING;\n        "
            )
            cur.execute(
                "SELECT id_estado FROM public.estado_cuenta WHERE estado = 'Inactivo'"
            )
            id_inactivo = cur.fetchone()[0]
            cur.execute(
                '\n            UPDATE public.personal SET estado = %s WHERE "CURP" = %s\n        ',
                (id_inactivo, curp),
            )
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Error al inhabilitar al usuario: {e}")


def able_user(curp):
    "Cambia el estado de la cuenta a Activo en la tabla personal."
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute(
                "SELECT id_estado FROM public.estado_cuenta WHERE estado = 'Activo'"
            )
            id_activo = cur.fetchone()[0]
            cur.execute(
                '\n            UPDATE public.personal SET estado = %s WHERE "CURP" = %s\n        ',
                (id_activo, curp),
            )
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Error al habilitar al usuario: {e}")


def delete_user(curp):
    "\n    Eliminar desde persona es suficiente: las tablas de rol y personal\n    tienen ON DELETE CASCADE desde persona.\n"
    try:
        with get_db_cursor() as (cur, conn):
            cur.execute('DELETE FROM public.persona WHERE "CURP" = %s', (curp,))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Error al eliminar: {e}")


def search_one_user(curp):
    "Busca un usuario en todas las tablas de rol y devuelve un dict con sus datos."
    try:
        with get_db_cursor() as (cur, conn):
            roles = {
                "abogado": "abogado",
                "medico": "medico",
                "psicologo": "psicologo",
                "trabajadorsocial": "trabajadorsocial",
            }
            for tabla, rol in roles.items():
                cur.execute(
                    f"""
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
            """,
                    (curp,),
                )
                res = cur.fetchone()
                if res:
                    return {
                        "curp": res[0],
                        "rfc": res[1],
                        "p_nombre": res[2],
                        "s_nombre": res[3],
                        "p_apellido": res[4],
                        "s_apellido": res[5],
                        "sexo": res[6],
                        "fecha_nacimiento": res[7],
                        "calle": res[8],
                        "num_ext": res[9],
                        "num_int": res[10],
                        "colonia": res[11],
                        "cp": res[12],
                        "municipio": res[13],
                        "estado_rep": res[14],
                        "correo": res[15],
                        "rol": rol,
                    }
            return None
    except psycopg2.Error as e:
        print(f"❌ Error al buscar usuario: {e}")


def update_user(curp, data):
    "\n    Actualiza los datos que pueden cambiar: correo, domicilio y nombre.\n    Los datos de catálogo (colonia, municipio, cp, estado) se crean si no existen.\n"
    try:
        with get_db_cursor() as (cur, conn):
            if all(
                (
                    data.get(k)
                    for k in ("estado_rep", "municipio", "cp", "colonia", "calle")
                )
            ):
                id_estado_rep = _get_or_create_estado(cur, data["estado_rep"])
                id_municipio = _get_or_create_municipio(
                    cur, data["municipio"], id_estado_rep
                )
                id_cp = _get_or_create_cp(cur, data["cp"])
                id_colonia = _get_or_create_colonia(
                    cur, data["colonia"], id_cp, id_municipio
                )
                cur.execute(
                    '\n                SELECT id_domicilio_persona FROM public.persona WHERE "CURP" = %s\n            ',
                    (curp,),
                )
                row = cur.fetchone()
                if row and row[0]:
                    cur.execute(
                        "\n                    UPDATE public.domicilio\n                    SET calle = %s, num_ext = %s, num_int = %s, id_colonia_domicilio = %s\n                    WHERE id_domicilio = %s\n                ",
                        (
                            data["calle"],
                            data.get("num_ext"),
                            data.get("num_int"),
                            id_colonia,
                            row[0],
                        ),
                    )
                else:
                    cur.execute(
                        "\n                    INSERT INTO public.domicilio (calle, num_ext, num_int, id_colonia_domicilio)\n                    VALUES (%s, %s, %s, %s) RETURNING id_domicilio\n                ",
                        (
                            data["calle"],
                            data.get("num_ext"),
                            data.get("num_int"),
                            id_colonia,
                        ),
                    )
                    id_dom_nuevo = cur.fetchone()[0]
                    cur.execute(
                        '\n                    UPDATE public.persona SET id_domicilio_persona = %s WHERE "CURP" = %s\n                ',
                        (id_dom_nuevo, curp),
                    )
            if data.get("correo"):
                id_correo = _get_or_create_correo(cur, data["correo"])
                cur.execute(
                    '\n                UPDATE public.persona SET id_correo = %s WHERE "CURP" = %s\n            ',
                    (id_correo, curp),
                )
            cur.execute(
                '\n            UPDATE public.persona\n            SET "RFC"           = COALESCE(%s, "RFC"),\n                p_nombre        = COALESCE(%s, p_nombre),\n                s_nombre        = %s,\n                p_apellido      = COALESCE(%s, p_apellido),\n                s_apellido      = COALESCE(%s, s_apellido),\n                fecha_nacimiento= COALESCE(%s, fecha_nacimiento)\n            WHERE "CURP" = %s\n        ',
                (
                    data.get("rfc"),
                    data.get("p_nombre"),
                    data.get("s_nombre"),
                    data.get("p_apellido"),
                    data.get("s_apellido"),
                    (data.get("fecha_nacimiento") or None),
                    curp,
                ),
            )
            if data.get("sexo"):
                id_sexo = _get_or_create_sexo(cur, data["sexo"])
                cur.execute(
                    '\n                UPDATE public.persona SET id_sexo_persona = %s WHERE "CURP" = %s\n            ',
                    (id_sexo, curp),
                )
            conn.commit()
            return True
    except Exception as e:
        print(f"❌ Error al actualizar al usuario: {e}")
        return False
