# ⚖️ Sistema de Gestión - Fundación Futuro con Derechos

Este sistema es una aplicación web integral desarrollada para la **Fundación Futuro con Derechos**. Permite el registro y la consulta centralizada del personal multidisciplinario (Abogados, Médicos, Psicólogos y Trabajadores Sociales) encargados de la restitución de derechos de Niñas, Niños y Adolescentes (NNA).

---

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** [Python 3.x](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/)
* **Base de Datos:** [PostgreSQL](https://www.postgresql.org/)
* **Interfaz:** HTML5, Bootstrap 5 y CSS3
* **Conector BD:** Psycopg2
* **Variables de Entorno:** python-dotenv
---
## Condiciones a tomar en cuenta
Antes de correr el proyecto verifique que tiene instalado python en su version más reciente.

## 🗄️ 1. Configuración de la Base de Datos (PostgreSQL)

Antes de correr el programa, instale la base de datos PostgreSQL: [www.postgresql.org](https://www-enterprisedb-com.translate.goog/downloads/postgres-postgresql-downloads?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc&_x_tr_hist=true). 
Una vez instalado, la base de datos debe estar lista en tu servidor local:

1. Abre **pgAdmin 4**.
2. Crea una base de datos.
3. Abre el **Query Tool** y ejecuta el script que te proporcionaremos para crear las tablas.

## 2. Clonar Repositorio

git clone [https://github.com/EmilianoRivera/Taimotla.git]([https://github.com/TuUsuario/TuRepositorio.git](https://github.com/EmilianoRivera/Taimotla.git))
cd TuRepositorio

## 3. Crear Entorno Virtual

# Crear entorno
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Mac/Linux)
source .venv/bin/activate

## 4. Instalar las Dependencias
1. pip install flask psycopg2-binary
2. pip install python-dotenv
## 5. Conexión con la Base de Datos 
# database.py / app.py
Ingrese al proyecto y cree un archivo .env donde ingresara los valores de estas variables: 
DB_HOST=ingresa_el_host
DB_NAME=nombre_de_la_bd
DB_USER=nombre_de_usuario
DB_PASSWORD=contraseña_de_la_bd
SECRET_KEY=pon_alguna_contraseña
## 6. Ejecución
Una vez configurado todo e instalado las dependencias y programas, ejecuta el siguiente comando:

```python hash_director.py ```
```python hash_coordinador.py ```
```flask --debug run ```

## 7. Abrir la aplicación
La aplicación estará disponible en el puerto 5000 en el localhost, ingrese a su navegador de preferencia y escriba la siguiente ruta para visualizar la ruta:

```localhost:5000 ```
Para iniciar sesión el correo del director es: director@fundacion.org con contraseña: admin123 y para iniciar sesión como coordinador : m.villagomez@fundacion.org con contraseña: coor123


