# Sistema de Gestión - Fundación Futuro con Derechos

Este sistema es una aplicación web integral desarrollada para la **Fundación Futuro con Derechos**. Permite el registro y la consulta centralizada del personal multidisciplinario (Abogados, Médicos, Psicólogos y Trabajadores Sociales) encargados de la restitución de derechos de Niñas, Niños y Adolescentes (NNA).

---

## Tecnologías y Herramientas

* **Lenguaje:** [Python 3.x](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/)
* **Base de Datos:** [PostgreSQL](https://www.postgresql.org/)
* **Interfaz:** HTML5, Bootstrap 5 y CSS3
* **Conector BD:** Psycopg2
* **Variables de Entorno:** python-dotenv

---

## Guía de Instalación y Ejecución

Sigue detalladamente estos pasos para configurar y poner en marcha el sistema en tu entorno local.

### 1. Requisitos Previos

Asegúrate de tener instalados los siguientes componentes en tu sistema:
* **Python (v3.8 o superior):** Puedes descargarlo desde [python.org](https://www.python.org/).
* **PostgreSQL:** Descárgalo e instálalo desde [postgresql.org](https://www.postgresql.org/).
* **pgAdmin 4 (opcional, pero recomendado):** Para administrar la base de datos visualmente.

---

### 2. Configurar el Entorno de Desarrollo

1. **Navega al directorio del proyecto:**
   Abre tu terminal en la carpeta raíz del proyecto.
2. **Crear el Entorno Virtual:**
   Crea un entorno de Python aislado para evitar conflictos de dependencias:
   ```bash
   python -m venv .venv
   ```
3. **Activar el Entorno Virtual:**
   * **En Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * **En Windows (CMD):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   * **En macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```
4. **Instalar Dependencias:**
   Instala todos los paquetes requeridos usando el archivo [requirements.txt](file:///c:/Users/Edgar/Documents/UNI/IV%20Semestre/ADS/Taimotla/requirements.txt):
   ```bash
   pip install -r requirements.txt
   ```

---

### 3. Configuración de la Base de Datos

1. **Crear la Base de Datos:**
   * Abre **pgAdmin 4** (o la herramienta de tu preferencia para PostgreSQL).
   * Crea una nueva base de datos llamada `GestionFundacion` (el nombre es opcional).
2. **Ejecutar el Script SQL:**
   * Abre la herramienta de consultas (**Query Tool**) sobre la base de datos creada.
   * Carga y ejecuta el contenido del script de la base de datos: [bd_nna.sql](file:///c:/Users/Edgar/Documents/UNI/IV%20Semestre/ADS/Taimotla/script_bd/bd_nna.sql). Este script creará todas las tablas y relaciones necesarias.

---

### 4. Configurar Variables de Envío (.env)

1. En la raíz del proyecto encontrarás el archivo de plantilla [.env.example](file:///c:/Users/Edgar/Documents/UNI/IV%20Semestre/ADS/Taimotla/.env.example).
2. Copia este archivo y renombralo a `.env`:
   * En Windows (PowerShell):
     ```powershell
     Copy-Item .env.example .env
     ```
   * En macOS/Linux/CMD:
     ```bash
     cp .env.example .env
     ```
3. Abre el archivo `.env` recién creado y actualiza las variables de conexión con tus credenciales de PostgreSQL:
   ```env
   DB_HOST=localhost
   DB_NAME=GestionFundacion
   DB_USER=tu_usuario_de_postgres
   DB_PASSWORD=tu_contraseña_de_postgres
   SECRET_KEY=clave_secreta_para_flask
   ```

---

### 5. Sembrado de Datos Iniciales (Seeders)

Para poder iniciar sesión, es necesario poblar la base de datos con los roles iniciales y catálogos. Ejecuta los siguientes scripts desde **la raíz del proyecto** usando el flag `-m` para que Python resuelva las rutas de importación relativas hacia el módulo `models`:

1. **Insertar Director Administrativo (Ulises Vélez):**
   ```bash
   python -m extras.hash_director
   ```
   *Código fuente disponible en: [hash_director.py](file:///c:/Users/Edgar/Documents/UNI/IV%20Semestre/ADS/Taimotla/extras/hash_director.py)*

2. **Insertar Coordinadora del Sistema (Mariana Villagómez):**
   ```bash
   python -m extras.hash_coordinador
   ```
   *Código fuente disponible en: [hash_coordinador.py](file:///c:/Users/Edgar/Documents/UNI/IV%20Semestre/ADS/Taimotla/extras/hash_coordinador.py)*

3. **Insertar Catálogos Generales (Estados, cuentas, etc.):**
   ```bash
   python -m extras.Catalogos
   ```
   *Código fuente disponible en: [Catalogos.py](file:///c:/Users/Edgar/Documents/UNI/IV%20Semestre/ADS/Taimotla/extras/Catalogos.py)*

---

### 6. Ejecución de la Aplicación

Una vez configurada la base de datos y poblados los registros iniciales, arranca el servidor web local de desarrollo:

1. **Ejecución con Flask CLI (Recomendado para recarga automática en desarrollo):**
   ```bash
   flask --debug run
   ```
   *O de forma directa ejecutando el archivo [app.py](file:///c:/Users/Edgar/Documents/UNI/IV%20Semestre/ADS/Taimotla/app.py):*
   ```bash
   python app.py
   ```
2. Abre tu navegador web e ingresa a:
   [http://localhost:5000](http://localhost:5000)

---

### 7. Credenciales de Acceso para Pruebas

Utiliza las siguientes cuentas iniciales de prueba para validar el funcionamiento del sistema:

* **Rol Director:**
  * **Correo:** `director@fundacion.org`
  * **Contraseña:** `admin123`
* **Rol Coordinador:**
  * **Correo:** `m.villagomez@fundacion.org`
  * **Contraseña:** `coor123`
