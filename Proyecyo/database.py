import psycopg2

def obtener_conexion():
    try:
        
        conexion = psycopg2.connect(
            host="localhost",
            port="5432", 
            database="GestionFundacion", 
            user="postgres", 
            password=""
        )
        return conexion
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")

        return None
