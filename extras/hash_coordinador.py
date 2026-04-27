from werkzeug.security import generate_password_hash
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def crear_coordinador_sistema():
    curp            = 'COOR850325HDFXXX09'
    correo_nuevo    = 'm.villagomez@fundacion.org'
    password_plana  = 'coor123'
    password_hash   = generate_password_hash(password_plana)
    curp_director   = 'DIRTEST12345678901'   # CURP del director ya existente en BD

    conn_params = {
        "host":     os.getenv('DB_HOST'),
        "database": os.getenv('DB_NAME'),
        "user":     os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
    }

    try:
        conn = psycopg2.connect(**conn_params)
        with conn.cursor() as cur:

            # 1. ESTADO
            cur.execute("""
                INSERT INTO public.estados (nombre_estado)
                VALUES ('Ciudad de México')
                ON CONFLICT (nombre_estado) DO NOTHING;
            """)
            cur.execute("SELECT id_estado FROM public.estados WHERE nombre_estado = 'Ciudad de México';")
            id_estado = cur.fetchone()[0]

            # 2. MUNICIPIO
            cur.execute("""
                INSERT INTO public.municipios (nombre_municipio, id_estados_municipio)
                VALUES ('Cuauhtémoc', %s)
                ON CONFLICT DO NOTHING;
            """, (id_estado,))
            cur.execute("SELECT id_municipio FROM public.municipios WHERE nombre_municipio = 'Cuauhtémoc';")
            id_municipio = cur.fetchone()[0]

            # 3. CÓDIGO POSTAL
            cur.execute("""
                INSERT INTO public.codigo_postal (codigo_postal)
                VALUES ('06600')
                ON CONFLICT (codigo_postal) DO NOTHING;
            """)
            cur.execute("SELECT id_cp FROM public.codigo_postal WHERE codigo_postal = '06600';")
            id_cp = cur.fetchone()[0]

            # 4. COLONIA
            cur.execute("""
                INSERT INTO public.colonia (colonia, id_cp_colonia, id_municipios_colonia)
                VALUES ('Juárez', %s, %s)
                ON CONFLICT DO NOTHING;
            """, (id_cp, id_municipio))
            cur.execute("SELECT id_colonia FROM public.colonia WHERE colonia = 'Juárez';")
            id_colonia = cur.fetchone()[0]

            # 5. DOMICILIO
            cur.execute("""
                INSERT INTO public.domicilio (num_ext, calle, id_colonia_domicilio)
                VALUES (%s, %s, %s) RETURNING id_domicilio;
            """, ('405', 'Paseo de la Reforma', id_colonia))
            id_domicilio = cur.fetchone()[0]

            # 6. CORREO
            cur.execute("""
                INSERT INTO public.correos (correo)
                VALUES (%s)
                ON CONFLICT (correo) DO NOTHING
                RETURNING id_correo;
            """, (correo_nuevo,))
            row = cur.fetchone()
            if row is None:
                cur.execute("SELECT id_correo FROM public.correos WHERE correo = %s;", (correo_nuevo,))
                row = cur.fetchone()
            id_correo = row[0]

            # 7. SEXO
            cur.execute("""
                INSERT INTO public.sexo (sexo) VALUES ('Femenino')
                ON CONFLICT (sexo) DO NOTHING;
            """)
            cur.execute("SELECT id_sexo FROM public.sexo WHERE sexo = 'Femenino';")
            id_sexo = cur.fetchone()[0]

            # 8. PERSONA
            cur.execute("""
                INSERT INTO public.persona (
                    "CURP", "RFC", p_nombre, s_nombre, p_apellido, s_apellido,
                    fecha_nacimiento, id_sexo_persona, id_domicilio_persona, id_correo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                curp, 'VILM850325HDF', 'Mariana', 'Beatriz',
                'Villagómez', 'Esparza', '1985-03-25',
                id_sexo, id_domicilio, id_correo
            ))

            # 9. ESTADO DE CUENTA
            cur.execute("""
                INSERT INTO public.estado_cuenta (estado) VALUES ('Activo')
                ON CONFLICT DO NOTHING;
            """)
            cur.execute("SELECT id_estado FROM public.estado_cuenta WHERE estado = 'Activo';")
            id_estado_cuenta = cur.fetchone()[0]

            # 10. PERSONAL
            cur.execute("""
                INSERT INTO public.personal ("CURP", fecha_alta, voluntario, contrasena, estado)
                VALUES (%s, CURRENT_DATE, False, %s, %s);
            """, (curp, password_hash, id_estado_cuenta))

            # 11. COORDINADOR  (id_director_cargo = CURP del director)
            cur.execute("""
                INSERT INTO public.coordinador ("CURP", id_director_cargo)
                VALUES (%s, %s);
            """, (curp, curp_director))

        conn.commit()
        print("✅ ¡Éxito! Coordinador creado.")
        print(f"   Login : {correo_nuevo}")
        print(f"   Pass  : {password_plana}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    crear_coordinador_sistema()