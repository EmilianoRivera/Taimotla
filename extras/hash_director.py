from models.database import obtener_conexion
from werkzeug.security import generate_password_hash

def sembrar_director():
    conn = obtener_conexion()
    cur = conn.cursor()

    password_plana = 'admin123'
    password_hashed = generate_password_hash(password_plana)

    try:
        
        # Insertar CORREO
        cur.execute("INSERT INTO public.correos (correo) VALUES (%s) RETURNING correo;", ('director@fundacion.org',))
        id_correo_generado = cur.fetchone()[0]

        # Insertar DOMICILIO 
        query_domicilio = """ 
            INSERT INTO public.domicilio (num_ext, num_int, calle, id_colonia_domicilio) 
            VALUES (%s, %s, %s, %s) RETURNING id_domicilio; 
        """
        datos_domicilio = ("63", "2", "Av. San Bernabe", 1) 
        cur.execute(query_domicilio, datos_domicilio)
        id_domicilio_generado = cur.fetchone()[0]

        # Insertar PERSONA
        query_persona = """ 
            INSERT INTO public.persona (
                "CURP", "RFC", "p_nombre", "s_nombre", "p_apellido", "s_apellido", 
                "fecha_nacimiento", id_sexo_persona, id_domicilio_persona, "id_correo"
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, 
                (SELECT id_sexo FROM public.sexo WHERE sexo = 'Masculino' LIMIT 1),
                %s, %s); 
        """

        datos_persona_director = (
            'DIRTEST12345678901', 'DIRT990101XYZ', 'Ulises', None, 
            'Vélez', 'Saldaña', '1980-05-15', 
            id_domicilio_generado, id_correo_generado
        )
        cur.execute(query_persona, datos_persona_director)

        # Insertar PERSONAL
        query_personal = """
            INSERT INTO public.personal ("CURP", fecha_alta, voluntario, contrasena, estado) 
            VALUES (%s, CURRENT_DATE, False, %s, 1)
        """
        cur.execute(query_personal, ('DIRTEST12345678901', password_hashed))

        # Insertar DIRECTOR 
        query_director = "INSERT INTO public.director (\"CURP\") VALUES (%s);"
        cur.execute(query_director, ('DIRTEST12345678901',))

        conn.commit()
        print("✅ Director Ulises insertado correctamente.")

    except Exception as e:
        print(f"❌ Error al insertar: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == "__main__":
    sembrar_director()
