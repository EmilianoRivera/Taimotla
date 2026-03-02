# ⚖️ Sistema de Gestión - Fundación Futuro con Derechos

Este sistema es una aplicación web integral desarrollada para la **Fundación Futuro con Derechos**. Permite el registro y la consulta centralizada del personal multidisciplinario (Abogados, Médicos, Psicólogos y Trabajadores Sociales) encargados de la restitución de derechos de Niñas, Niños y Adolescentes (NNA).

---

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** [Python 3.x](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/)
* **Base de Datos:** [PostgreSQL](https://www.postgresql.org/)
* **Interfaz:** HTML5, Bootstrap 5 y CSS3
* **Conector BD:** Psycopg2

---

## 🗄️ 1. Configuración de la Base de Datos (PostgreSQL)

Antes de correr el programa, la base de datos debe estar lista en tu servidor local:

1. Abre **pgAdmin 4**.
2. Crea una base de datos.
3. Abre el **Query Tool** y ejecuta el script que te proporcionaremos para crear las tablas.

## 2. Clonar Repositorio

git clone [https://github.com/TuUsuario/TuRepositorio.git](https://github.com/TuUsuario/TuRepositorio.git)
cd TuRepositorio

## 3. Crear Entorno Virtual

# Crear entorno
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Mac/Linux)
source .venv/bin/activate

## 4. Instalar las Dependencias
pip install flask psycopg2-binary
pip install python-dotenv
## 5. Conexión con la Base de Datos 
# database.py / app.py
password="TU_CONTRASEÑA_DE_POSTGRES"
dbname="Nombre que le asignaste a la bd"

## 6. Ejecución
Una vez configurado todo e instalado las dependencias y programas, ejecuta el siguiente comando:

```python app.py ```


