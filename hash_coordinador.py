from werkzeug.security import generate_password_hash
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def crear_coordinador_sistema():
    curp = 'COOR850325HDFXXX09' # CURP distinta
    correo_nuevo = 'm.villagomez@fundacion.org' # Correo distinto
    password_plana = 'coor123' 
    password_hasheada = generate_password_hash(password_plana)
    id_director_resp = 2

    conn_params = {
        "host": os.getenv('DB_HOST'),
        "database": os.getenv('DB_NAME'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD')

    }


    try:
        conn = psycopg2.connect(**conn_params)
        with conn.cursor() as cursor:
            sql_persona = """
                INSERT INTO persona 
                ("CURP", "RFC", p_nombre, s_nombre, p_apellido, s_apellido, sexo, 
                 fecha_nacimiento, calle, num_ext, colonia, cp, municipio, 
                 estado_rep, telefono, correo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val_persona = (
                curp, 'VILM850325HDF', 'Mariana', 'Beatriz', 'Villagómez', 'Esparza', 'Femenino',
                '1985-03-25', 'Paseo de la Reforma', '405', 'Juárez', '06600', 'Cuauhtémoc',
                'Ciudad de México', '5512345678', correo_nuevo
            )
            cursor.execute(sql_persona, val_persona)

            sql_coord = """
                INSERT INTO coordinador 
                ("CURP", contrasena, estado, id_director) 
                VALUES (%s, %s, %s, %s)
            """
            val_coord = (curp, password_hasheada, 'Activo', id_director_resp)
            cursor.execute(sql_coord, val_coord)

        conn.commit()
        print("✅ ¡Éxito! Coordinador creado.")
        print(f"Login: {correo_nuevo}")
        print(f"Pass: {password_plana}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    crear_coordinador_sistema()