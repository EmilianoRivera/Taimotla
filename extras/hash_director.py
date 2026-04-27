from models.database import obtener_conexion
from werkzeug.security import generate_password_hash

def sembrar_director():
    conn = obtener_conexion()
    cur = conn.cursor()

    password_plana = 'admin123'
    password_hashed = generate_password_hash(password_plana)

    try:
        # 1. Insertar ESTADO (si no existe)
        cur.execute("""
            INSERT INTO public.estados (nombre_estado)
            VALUES ('Ciudad de México')
            ON CONFLICT (nombre_estado) DO NOTHING;
        """)
        cur.execute("SELECT id_estado FROM public.estados WHERE nombre_estado = 'Ciudad de México';")
        id_estado = cur.fetchone()[0]

        # 2. Insertar MUNICIPIO (si no existe)
        cur.execute("""
            INSERT INTO public.municipios (nombre_municipio, id_estados_municipio)
            VALUES ('Magdalena Contreras', %s)
            ON CONFLICT DO NOTHING;
        """, (id_estado,))
        cur.execute("""
            SELECT id_municipio FROM public.municipios
            WHERE nombre_municipio = 'Magdalena Contreras';
        """)
        id_municipio = cur.fetchone()[0]

        # 3. Insertar CÓDIGO POSTAL (si no existe)
        cur.execute("""
            INSERT INTO public.codigo_postal (codigo_postal)
            VALUES ('10200')
            ON CONFLICT (codigo_postal) DO NOTHING;
        """)
        cur.execute("SELECT id_cp FROM public.codigo_postal WHERE codigo_postal = '10200';")
        id_cp = cur.fetchone()[0]

        # 4. Insertar COLONIA (si no existe)
        cur.execute("""
            INSERT INTO public.colonia (colonia, id_cp_colonia, id_municipios_colonia)
            VALUES ('San Bernabé Ocotepec', %s, %s)
            ON CONFLICT DO NOTHING;
        """, (id_cp, id_municipio))
        cur.execute("""
            SELECT id_colonia FROM public.colonia
            WHERE colonia = 'San Bernabé Ocotepec';
        """)
        id_colonia = cur.fetchone()[0]

        # 5. Insertar DOMICILIO
        cur.execute("""
            INSERT INTO public.domicilio (num_ext, num_int, calle, id_colonia_domicilio)
            VALUES (%s, %s, %s, %s) RETURNING id_domicilio;
        """, ('63', '2', 'Av. San Bernabé', id_colonia))
        id_domicilio = cur.fetchone()[0]

        # 6. Insertar CORREO
        cur.execute("""
            INSERT INTO public.correos (correo)
            VALUES (%s)
            ON CONFLICT (correo) DO NOTHING
            RETURNING id_correo;
        """, ('director@fundacion.org',))
        row = cur.fetchone()
        if row is None:
            cur.execute("SELECT id_correo FROM public.correos WHERE correo = 'director@fundacion.org';")
            row = cur.fetchone()
        id_correo = row[0]

        # 7. Insertar SEXO (si no existe)
        cur.execute("""
            INSERT INTO public.sexo (sexo) VALUES ('Masculino')
            ON CONFLICT (sexo) DO NOTHING;
        """)
        cur.execute("SELECT id_sexo FROM public.sexo WHERE sexo = 'Masculino';")
        id_sexo = cur.fetchone()[0]

        # 8. Insertar PERSONA
        cur.execute("""
            INSERT INTO public.persona (
                "CURP", "RFC", p_nombre, s_nombre, p_apellido, s_apellido,
                fecha_nacimiento, id_sexo_persona, id_domicilio_persona, id_correo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            'DIRTEST12345678901', 'DIRT990101XYZ', 'Ulises', None,
            'Vélez', 'Saldaña', '1980-05-15',
            id_sexo, id_domicilio, id_correo
        ))

        # 9. Insertar ESTADO DE CUENTA (si no existe)
        cur.execute("""
            INSERT INTO public.estado_cuenta (estado) VALUES ('Activo')
            ON CONFLICT DO NOTHING;
        """)
        cur.execute("SELECT id_estado FROM public.estado_cuenta WHERE estado = 'Activo';")
        id_estado_cuenta = cur.fetchone()[0]

        # 10. Insertar PERSONAL
        cur.execute("""
            INSERT INTO public.personal ("CURP", fecha_alta, voluntario, contrasena, estado)
            VALUES (%s, CURRENT_DATE, False, %s, %s);
        """, ('DIRTEST12345678901', password_hashed, id_estado_cuenta))

        # 11. Insertar DIRECTOR
        cur.execute("""
            INSERT INTO public.director ("CURP") VALUES (%s);
        """, ('DIRTEST12345678901',))

        conn.commit()
        print("✅ Director Ulises insertado correctamente.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error al insertar: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    sembrar_director()