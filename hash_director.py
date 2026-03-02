import psycopg2
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()
def sembrar_director():
    conn_params = {
        "host": os.getenv('DB_HOST'),
        "database": os.getenv('DB_NAME'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD')
    }

    password_plana = 'admin123'
    password_hashed = generate_password_hash(password_plana)

    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # Query 1: Insertar Persona
        query_persona = """
        INSERT INTO public.persona (
            "CURP", "RFC", "p_nombre", "s_nombre", "p_apellido", "s_apellido", 
            "sexo", "fecha_nacimiento", "correo", "telefono", "calle", "num_ext"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        datos_persona = (
            'DIRTEST12345678901', 'DIRT990101XYZ', 'Ulises', None, 
            'Vélez', 'Saldaña', 'Masculino', '1980-05-15', 
            'director@fundacion.org', '5551234567', 
            'Av. Instituto Politécnico Nacional', '2508'
        )


        query_director = """
        INSERT INTO public.director (
            "CURP", "fecha_ingreso", "contrasena", "estado"
        ) VALUES (%s, CURRENT_DATE, %s, %s);
        """
        datos_director = ('DIRTEST12345678901', password_hashed, 'Activo')

        # Ejecutamos
        cur.execute(query_persona, datos_persona)
        cur.execute(query_director, datos_director)

        conn.commit()
        print("✅ Director Ulises insertado correctamente con contraseña hasheada.")

    except Exception as e:
        print(f"❌ Error al insertar: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == "__main__":
    sembrar_director()