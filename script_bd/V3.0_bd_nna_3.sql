-- ===== PARTE 1: CATÁLOGOS SIMPLES (Sin dependencias) =====

-- Catálogo: SEXO
CREATE TABLE IF NOT EXISTS public.sexo (
	id_sexo SERIAL,
	sexo VARCHAR(10) NOT NULL,
	CONSTRAINT id_sexo PRIMARY KEY(id_sexo),
	CONSTRAINT sexo_unique UNIQUE(sexo)
);

-- Catálogo: CORREOS
CREATE TABLE IF NOT EXISTS public.correos (
	 correo VARCHAR(100) NOT NULL,
	 CONSTRAINT correo_pkey PRIMARY KEY(correo) 
);

-- Catálogo: TELEFONOS
CREATE TABLE IF NOT EXISTS public.telefonos (
	 numero_telefono VARCHAR(15) NOT NULL,
	 tipo VARCHAR(20),
	 CONSTRAINT telefono_pkey PRIMARY KEY(numero_telefono) 
);

-- Catálogo: ESTADOS DE LA REPÚBLICA
CREATE TABLE IF NOT EXISTS public.estados (
	id_estado SERIAL,
	nombre_estado VARCHAR(50) NOT NULL,
	CONSTRAINT id_estado PRIMARY KEY (id_estado),
	CONSTRAINT nombre_estado_unique UNIQUE (nombre_estado)
);

-- Catálogo: CODIGO POSTAL
CREATE TABLE IF NOT EXISTS public.codigo_postal (
	id_cp SERIAL,
	codigo_postal VARCHAR(50) NOT NULL,
	CONSTRAINT id_cp_pkey PRIMARY KEY (id_cp),
	CONSTRAINT codigo_postal_unique UNIQUE (codigo_postal) 
);

-- Catálogo: MUNICIPIOS (depende de estados)
CREATE TABLE IF NOT EXISTS public.municipios (
	id_municipio SERIAL,
	nombre_municipio VARCHAR(50) NOT NULL,
	id_estados_municipio int,
	CONSTRAINT fk_estado_republica_municipios
        FOREIGN KEY (id_estados_municipio) 
        REFERENCES public.estados (id_estado)
        ON UPDATE CASCADE
        ON DELETE SET NULL, 
	CONSTRAINT id_municipio_pkey PRIMARY KEY (id_municipio)
);

-- Catálogo: COLONIA (depende de pcodigo_postal y municipios)
CREATE TABLE IF NOT EXISTS public.colonia (
	id_colonia SERIAL,
	colonia VARCHAR(100) NOT NULL,
	id_cp_colonia int,
	id_municipios_colonia int,
	CONSTRAINT fk_municipios_colonia 
		FOREIGN KEY (id_municipios_colonia) 
		REFERENCES public.municipios (id_municipio)
		ON UPDATE CASCADE
		ON DELETE SET NULL,
	CONSTRAINT fk_cp_colonia 
		FOREIGN KEY (id_cp_colonia) 
		REFERENCES public.codigo_postal (id_cp)
		ON UPDATE CASCADE
		ON DELETE SET NULL,
	CONSTRAINT id_colonia_pkey PRIMARY KEY (id_colonia)
);

-- Catálogo: DOMICILIO (depende de colonia)
CREATE TABLE IF NOT EXISTS public.domicilio (
	id_domicilio SERIAL,
	num_ext VARCHAR(10) NOT NULL,
	num_int VARCHAR(10),
	calle VARCHAR(100) NOT NULL,
	id_colonia_domicilio int,
	CONSTRAINT fk_colonia_domicilio 
		FOREIGN KEY (id_colonia_domicilio) 
		REFERENCES public.colonia (id_colonia)
		ON UPDATE CASCADE
		ON DELETE SET NULL,
	CONSTRAINT id_domicilio_pkey PRIMARY KEY(id_domicilio)
);

-- Catálogo: IDIOMAS
CREATE TABLE IF NOT EXISTS public.idiomas (
    id_idioma SERIAL,
    codigo VARCHAR(4) NOT NULL,
    nombre_idioma VARCHAR(50) NOT NULL UNIQUE,
	CONSTRAINT id_idioma_pkey PRIMARY KEY (id_idioma)
);

-- Catálogo: VARIANTE IDIOMA (depende de idiomas)
CREATE TABLE IF NOT EXISTS public.variante_idioma (
    id_variante SERIAL,
    nombre_variante VARCHAR(50) NOT NULL UNIQUE,
	id_idioma int,
	CONSTRAINT fk_idioma_dominio 
		FOREIGN KEY (id_idioma)
		REFERENCES public.idiomas(id_idioma)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT id_variante_pkey PRIMARY KEY (id_variante)
);

-- Catálogo: DOMINIO IDIOMA
CREATE TABLE IF NOT EXISTS public.dominio_idioma (
    id_dominio SERIAL,
    dominio VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT id_dominio_pkey PRIMARY KEY (id_dominio)
);

-- Catálogo: ETNIAS
CREATE TABLE IF NOT EXISTS public.etnia (
    id_etnia SERIAL,
    nombre_etnia VARCHAR(50) NOT NULL UNIQUE,
	CONSTRAINT id_etnia_pkey PRIMARY KEY (id_etnia)
);

-- Catálogo: ESTADO CUENTA
CREATE TABLE IF NOT EXISTS public.estado_cuenta (
	id_estado SERIAL,
	estado VARCHAR(20) NOT NULL,
	CONSTRAINT id_estado_pkey PRIMARY KEY (id_estado)
);

-- Catálogo: ESTADO EQUIPO
CREATE TABLE IF NOT EXISTS public.estado_equipo (
    id_estado_equipo SERIAL,
    nombre_estado VARCHAR(30) NOT NULL UNIQUE,
    CONSTRAINT id_estado_equipo_pkey PRIMARY KEY(id_estado_equipo)
);

-- Catálogo: ESTADO EXPEDIENTE
CREATE TABLE IF NOT EXISTS public.estado_expediente (
    id_estado_expediente SERIAL,
    nombre_estado VARCHAR(30) NOT NULL UNIQUE,
    descripcion text,
	CONSTRAINT id_estado_expediente_pkey PRIMARY KEY (id_estado_expediente)
);

-- Catálogo: SEGURO MEDICO
CREATE TABLE IF NOT EXISTS public.seguro_medico (
    id_seguro SERIAL,
    nombre_institucion VARCHAR(50) NOT NULL UNIQUE,
	CONSTRAINT id_seguro_pkey PRIMARY KEY(id_seguro)
);

-- Catálogo: PADECIMIENTO
CREATE TABLE IF NOT EXISTS public.padecimiento (
    id_padecimiento SERIAL,
    nombre_padecimiento VARCHAR(100) NOT NULL,
    codigo_padecimiento VARCHAR(20) NOT NULL,
	CONSTRAINT id_padecimiento_pkey PRIMARY KEY (id_padecimiento)
);

-- Catálogo: TIPO DISCAPACIDAD
CREATE TABLE IF NOT EXISTS public.tipo_discapacidad (
    id_tipo_discapacidad SERIAL,
    nombre_tipo VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT id_tipo_discapacidad_pkey PRIMARY KEY (id_tipo_discapacidad)
);

-- Catálogo: GRADO DEPENDENCIA
CREATE TABLE IF NOT EXISTS public.grado_dependencia (
    id_grado_dependencia SERIAL,
    descripcion_grado VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT id_grado_dependencia_pkey PRIMARY KEY (id_grado_dependencia)
);

-- Catálogo: NIVEL EDUCATIVO
CREATE TABLE IF NOT EXISTS public.nivel_educativo (
    id_nivel_educativo SERIAL,
    nombre_nivel VARCHAR(30) NOT NULL UNIQUE,
	CONSTRAINT id_nivel_educativo_pkey PRIMARY KEY(id_nivel_educativo)
);

-- Catálogo: GRADO ESCOLAR
CREATE TABLE IF NOT EXISTS public.grado_escolar (
    id_grado_escolar SERIAL,
    nombre_grado VARCHAR(50) NOT NULL UNIQUE,
    orden INT NOT NULL,
    CONSTRAINT id_grado_escolar_pkey PRIMARY KEY(id_grado_escolar)
);

-- Catálogo: TIPO DOCUMENTO NNA
CREATE TABLE IF NOT EXISTS public.tipo_documento_nna (
    id_tipo_documento_nna SERIAL,
    tipo_documento VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    CONSTRAINT id_tipo_documento_nna_pkey PRIMARY KEY(id_tipo_documento_nna)
);

-- Catálogo: INSTITUCION MEDICA
CREATE TABLE IF NOT EXISTS public.institucion_medica (
    id_institucion_medica SERIAL,
    nombre_institucion VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT id_institucion_medica_pkey PRIMARY KEY(id_institucion_medica)
);

-- Catálogo: ESTADO DOCUMENTO
CREATE TABLE IF NOT EXISTS public.estado_documento (
    id_estado_documento SERIAL,
    estado VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT id_estado_documento_pkey PRIMARY KEY(id_estado_documento)
);

-- Catálogo: NACIONALIDAD
CREATE TABLE IF NOT EXISTS public.nacionalidad (
    id_nacionalidad SERIAL,
    nombre_nacionalidad VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT id_nacionalidad_pkey PRIMARY KEY(id_nacionalidad)
);

-- Catálogo: TIPO DETECTOR
CREATE TABLE IF NOT EXISTS public.tipo_detector (
    id_tipo_detector SERIAL,
    tipo_detector VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT id_tipo_detector_pkey PRIMARY KEY (id_tipo_detector)
);

-- Catálogo: PARENTESCO
CREATE TABLE IF NOT EXISTS public.parentesco(
    id_parentesco SERIAL,
    tipo_parentes VARCHAR(50),
    CONSTRAINT id_parentesco_pkey PRIMARY KEY (id_parentesco)
);

-- Catálogo: GRADO NEGACION
CREATE TABLE IF NOT EXISTS public.grado_negacion (
    id_grado_negacion SERIAL,
    descripcion VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT id_grado_negacion_pkey PRIMARY KEY (id_grado_negacion)
);

-- Catálogo: GRADO AFECTACION EMOCIONAL
CREATE TABLE IF NOT EXISTS public.grado_afectacion_emocional (
    id_grado_afectacion_emocional SERIAL,
    descripcion VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT id_grado_afectacion_emocional_pkey PRIMARY KEY (id_grado_afectacion_emocional)
);

-- Catálogo: TIPO ACTOR
CREATE TABLE IF NOT EXISTS public.tipo_actor (
    id_tipo_actor SERIAL,
    tipo_actor VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT id_tipo_actor_pkey PRIMARY KEY (id_tipo_actor)
);

-- Catálogo: SECTOR SERVICIO
CREATE TABLE IF NOT EXISTS public.sector_servicio (
    id_sector SERIAL,
    nombre_sector VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT id_sector_pkey PRIMARY KEY (id_sector)
);

-- Catálogo: ESTADO ACTOR
CREATE TABLE IF NOT EXISTS public.estado_actor (
    id_estado_actor SERIAL,
    estado VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT id_estado_actor_pkey PRIMARY KEY (id_estado_actor)
);

-- Catálogo: RED SOCIAL
CREATE TABLE IF NOT EXISTS public.red_social (
    id_red_social SERIAL,
    nombre_red VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT id_red_social_pkey PRIMARY KEY (id_red_social)
);

-- Tabla de teléfonos separada
CREATE TABLE IF NOT EXISTS public.telefonos_tutores(
    id_telefono SERIAL,
    numero_telefono VARCHAR(20) NOT NULL UNIQUE,
    tipo_telefono VARCHAR(20) DEFAULT 'celular',
    CONSTRAINT id_telefono_pkey PRIMARY KEY (id_telefono)
);

-- Tabla de correos separada
CREATE TABLE IF NOT EXISTS public.correos_tutores(
    id_correo SERIAL,
    direccion_correo VARCHAR(100) NOT NULL UNIQUE,
    tipo_correo VARCHAR(20) DEFAULT 'personal',
    CONSTRAINT id_correo_pkey PRIMARY KEY (id_correo)
);

-- ===== PARTE 2: TABLAS ESCUELAS Y NNA BASE =====

-- Catálogo: ESCUELA (depende de domicilio)
CREATE TABLE IF NOT EXISTS public.escuela (
    id_escuela SERIAL,
    nombre_escuela VARCHAR(100) NOT NULL UNIQUE,
    id_domicilio INT,
    CONSTRAINT fk_domicilio_escuela FOREIGN KEY (id_domicilio) 
        REFERENCES public.domicilio(id_domicilio) ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT id_escuela_pkey PRIMARY KEY(id_escuela)
);

-- ===== PARTE 3: PERSONAS Y PERSONAL =====

-- PERSONA (depende de sexo, domicilio, correos)
CREATE TABLE IF NOT EXISTS public.persona
(
    "CURP" VARCHAR(18) NOT NULL,
    "RFC" VARCHAR(13) NOT NULL,
    p_nombre VARCHAR(50) NOT NULL,
    s_nombre VARCHAR(50),
    p_apellido VARCHAR(50) NOT NULL,
    s_apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento date NOT NULL,
	id_sexo_persona int,
	id_domicilio_persona int,
	id_correo VARCHAR(100),
	CONSTRAINT fk_sexo_persona
        FOREIGN KEY (id_sexo_persona) 
        REFERENCES public.sexo (id_sexo)
        ON UPDATE CASCADE
        ON DELETE SET NULL, 
	CONSTRAINT fk_id_domicilio_persona
        FOREIGN KEY (id_domicilio_persona) 
        REFERENCES public.domicilio (id_domicilio)
        ON UPDATE CASCADE
        ON DELETE SET NULL, 
	CONSTRAINT fk_id_correo_persona
        FOREIGN KEY (id_correo) 
        REFERENCES public.correos (correo)
        ON UPDATE CASCADE
        ON DELETE SET NULL, 
    CONSTRAINT persona_pkey PRIMARY KEY ("CURP"),
    CONSTRAINT "persona_RFC_key" UNIQUE ("RFC")
);

-- PERSONAL (depende de persona, estado_cuenta)
CREATE TABLE IF NOT EXISTS public.personal
(
    "CURP" VARCHAR(18) NOT NULL, 
    fecha_alta DATE NOT NULL,
    voluntario BOOL NOT NULL,
	contrasena VARCHAR(255) NOT NULL,
	estado int,
    CONSTRAINT fk_persona_personal 
        FOREIGN KEY ("CURP")
        REFERENCES public.persona("CURP")
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT fk_estado_personal 
        FOREIGN KEY (estado)
        REFERENCES public.estado_cuenta(id_estado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT personal_pkey PRIMARY KEY ("CURP")
);

-- DIRECTOR (depende de personal)
CREATE TABLE IF NOT EXISTS public.director (
    "CURP" VARCHAR(18),
    CONSTRAINT fk_personal_director 
        FOREIGN KEY ("CURP") REFERENCES public.personal ("CURP")
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT director_pkey PRIMARY KEY ("CURP")
);

-- COORDINADOR (depende de personal, director)
CREATE TABLE IF NOT EXISTS public.coordinador (
    "CURP" VARCHAR(18),
    id_director_cargo VARCHAR(18),
    CONSTRAINT fk_personal_coordinador 
        FOREIGN KEY ("CURP") REFERENCES public.personal ("CURP")
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_director_del_coordinador
        FOREIGN KEY (id_director_cargo) REFERENCES public.director ("CURP"),
	CONSTRAINT coordinador_pkey PRIMARY KEY ("CURP")
);

-- PSICOLOGO (depende de personal)
CREATE TABLE IF NOT EXISTS public.psicologo (
    "CURP" VARCHAR(18),
    cedula VARCHAR(20) UNIQUE,
    enfoque_terapeutico VARCHAR(100),
    CONSTRAINT fk_personal_psicologo 
        FOREIGN KEY ("CURP") REFERENCES public.personal ("CURP")
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT psicologo_pkey PRIMARY KEY ("CURP")
);

-- ABOGADO (depende de personal)
CREATE TABLE IF NOT EXISTS public.abogado (
    "CURP" VARCHAR(18),
    cedula VARCHAR(20) UNIQUE NOT NULL,
    especialidad VARCHAR(50),
    CONSTRAINT fk_personal_abogado 
        FOREIGN KEY ("CURP") REFERENCES public.personal ("CURP")
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT abogado_pkey PRIMARY KEY ("CURP")
);

-- TRABAJADOR SOCIAL (depende de personal)
CREATE TABLE IF NOT EXISTS public.trabajadorsocial (
    "CURP" VARCHAR(18),
    cedula VARCHAR(20) UNIQUE NOT NULL,
    CONSTRAINT fk_personal_tsocial 
        FOREIGN KEY ("CURP") REFERENCES public.personal ("CURP")
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT trabajadorsocial_pkey PRIMARY KEY ("CURP")
);

-- MEDICO (depende de personal)
CREATE TABLE IF NOT EXISTS public.medico (
    "CURP" VARCHAR(18),
    cedula VARCHAR(20) UNIQUE NOT NULL,
    especialidad VARCHAR(50),
    CONSTRAINT fk_personal_medico 
        FOREIGN KEY ("CURP") REFERENCES public.personal ("CURP")
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT medico_pkey PRIMARY KEY ("CURP")
);

-- EQUIPO (depende de coordinador, estado_equipo)
CREATE TABLE IF NOT EXISTS public.equipo (
    id_equipo SERIAL,
    nombre_equipo VARCHAR(50),
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    curp_coordinador VARCHAR(18) NOT NULL,
    id_estado_equipo int,
    CONSTRAINT fk_coordinador_equipo 
        FOREIGN KEY (curp_coordinador) 
        REFERENCES public.coordinador ("CURP")
        ON UPDATE CASCADE ON DELETE RESTRICT,
	CONSTRAINT fk_estado_equipo
        FOREIGN KEY (id_estado_equipo) 
        REFERENCES public.estado_equipo (id_estado_equipo)
        ON UPDATE CASCADE ON DELETE SET NULL, 
	CONSTRAINT id_equipo_pkey PRIMARY KEY(id_equipo)
);

-- COMPOSICION EQUIPO (depende de equipo, personal)
CREATE TABLE IF NOT EXISTS public.composicion_equipo (
    id_asignacion SERIAL,
    id_equipo int NOT NULL,
    curp_profesional VARCHAR(18) NOT NULL,
    fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin DATE,
    CONSTRAINT fk_equipo_asignado 
        FOREIGN KEY (id_equipo) REFERENCES public.equipo (id_equipo),
    CONSTRAINT fk_personal_asignado 
        FOREIGN KEY (curp_profesional) REFERENCES public.personal ("CURP")
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT id_asignacion_pkey PRIMARY KEY(id_asignacion)
);

-- ===== PARTE 4: NNA Y EXPEDIENTES =====

-- ===== TABLA DE DOCUMENTOS GENERALES (depende de tipo_documento_nna) =====
CREATE TABLE IF NOT EXISTS public.documentos (
    id_documento SERIAL,
    id_tipo_documento_nna INT,
    nombre_documento VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_documentos_tipo FOREIGN KEY (id_tipo_documento_nna) REFERENCES public.tipo_documento_nna(id_tipo_documento_nna) ON DELETE SET NULL,
    CONSTRAINT id_documento_pkey PRIMARY KEY(id_documento)
);

-- PERSONAS EXPEDIENTE (depende de sexo, domicilio)
CREATE TABLE IF NOT EXISTS public.personas_expediente (
   	id_persona_exp SERIAL,
	"CURP" VARCHAR(18),
    p_nombre VARCHAR(50) NOT NULL,
	s_nombre VARCHAR(50), 
    p_apellido VARCHAR(50) NOT NULL,
    s_apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
	id_sexo_persona int,
    id_domicilio INT,
	CONSTRAINT fk_domicilio_personas_expediente
        FOREIGN KEY (id_domicilio) 
		REFERENCES public.domicilio(id_domicilio)
        ON UPDATE CASCADE 
		ON DELETE SET NULL,
	CONSTRAINT fk_sexo_personas_expediente
        FOREIGN KEY (id_sexo_persona) 
        REFERENCES public.sexo (id_sexo)
        ON UPDATE CASCADE
        ON DELETE SET NULL,     
	CONSTRAINT id_persona_exp_pkey PRIMARY KEY(id_persona_exp)
);

-- HISTORIAL ESCOLAR NNA (depende de escuela, nivel_educativo, grado_escolar)
CREATE TABLE IF NOT EXISTS public.nna_historial_escolar (
    id_historial_escolar SERIAL,
    id_nna INT NOT NULL,
    id_escuela INT,
    id_nivel_educativo INT,
    id_grado_escolar INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    en_curso BOOLEAN NOT NULL DEFAULT FALSE,
    ha_asistido_escuela BOOLEAN NOT NULL DEFAULT FALSE,
    asiste_escuela_actual BOOLEAN NOT NULL DEFAULT FALSE,
    observaciones TEXT,
    CONSTRAINT fk_hist_escuela FOREIGN KEY (id_escuela) REFERENCES public.escuela(id_escuela) ON DELETE SET NULL,
    CONSTRAINT fk_hist_nivel FOREIGN KEY (id_nivel_educativo) REFERENCES public.nivel_educativo(id_nivel_educativo) ON DELETE SET NULL,
    CONSTRAINT fk_hist_grado FOREIGN KEY (id_grado_escolar) REFERENCES public.grado_escolar(id_grado_escolar) ON DELETE SET NULL,
    CONSTRAINT id_historial_escolar_pkey PRIMARY KEY(id_historial_escolar)
);

-- EXPEDIENTE (depende de equipo, estado_expediente)
CREATE TABLE IF NOT EXISTS public.expediente (
    id_expediente SERIAL,
    num_expediente VARCHAR(20) UNIQUE NOT NULL,
    fecha_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_equipo_responsable INT, 
    id_estado_expediente INT,
    CONSTRAINT fk_equipo_expediente 
        FOREIGN KEY (id_equipo_responsable) REFERENCES public.equipo(id_equipo),
	CONSTRAINT fk_estado_del_expediente
        FOREIGN KEY (id_estado_expediente) 
        REFERENCES public.estado_expediente(id_estado_expediente)
        ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT id_expediente_pkey PRIMARY KEY (id_expediente)
);

-- NNA (depende de personas_expediente, nacionalidad, expediente, etnia, historial_escolar)
CREATE TABLE IF NOT EXISTS public.nna (
    id_nna SERIAL,
    id_persona_exp_nna INT NOT NULL,
    id_expediente int,
    apodo VARCHAR(50),
    observaciones TEXT,
	id_etnia INT,
    id_historial_escolar_actual INT,
    id_documentos_nna INT,
    id_nacionalidad INT,
    CONSTRAINT fk_personaexp_nna FOREIGN KEY (id_persona_exp_nna)
        REFERENCES public.personas_expediente(id_persona_exp) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_nacionalidad_nna FOREIGN KEY (id_nacionalidad)
        REFERENCES public.nacionalidad(id_nacionalidad) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_expediente_nna FOREIGN KEY (id_expediente) 
        REFERENCES public.expediente(id_expediente) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_etnia_nna FOREIGN KEY (id_etnia) REFERENCES public.etnia(id_etnia) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_hist_actual_nna FOREIGN KEY (id_historial_escolar_actual) REFERENCES public.nna_historial_escolar(id_historial_escolar) ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT id_nna_pkey PRIMARY KEY (id_nna)
);

-- ALTER para agregar FK a nna en historial_escolar
ALTER TABLE public.nna_historial_escolar
    ADD CONSTRAINT fk_hist_nna FOREIGN KEY (id_nna) REFERENCES public.nna(id_nna) ON DELETE CASCADE;

-- NNA IDIOMAS (depende de nna, idiomas, variante_idioma, dominio_idioma)
CREATE TABLE IF NOT EXISTS public.nna_idiomas (
    id_nna INT NOT NULL,
    id_idioma INT NOT NULL,
    id_variante INT,
    id_dominio INT NOT NULL, 
    PRIMARY KEY (id_nna, id_idioma),
    CONSTRAINT fk_nna_idioma FOREIGN KEY (id_nna) 
        REFERENCES public.nna(id_nna) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_idioma_nna FOREIGN KEY (id_idioma) 
        REFERENCES public.idiomas(id_idioma) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_variante_nna FOREIGN KEY (id_variante) 
        REFERENCES public.variante_idioma(id_variante) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_dominio_nna FOREIGN KEY (id_dominio) 
        REFERENCES public.dominio_idioma(id_dominio) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- NNA SEGURO MEDICO (depende de nna, seguro_medico)
CREATE TABLE IF NOT EXISTS public.nna_seguro_medico (
    id_nna_seguro SERIAL,
    id_nna INT NOT NULL,
    id_seguro_medico INT NOT NULL,
    fecha_inicio DATE DEFAULT CURRENT_DATE,
    fecha_fin DATE,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    observaciones TEXT,
    CONSTRAINT fk_nna_seguro_nna FOREIGN KEY (id_nna) REFERENCES public.nna(id_nna) ON DELETE CASCADE,
    CONSTRAINT fk_nna_seguro_seguro FOREIGN KEY (id_seguro_medico) REFERENCES public.seguro_medico(id_seguro) ON DELETE RESTRICT,
    CONSTRAINT id_nna_seguro_pkey PRIMARY KEY(id_nna_seguro)
);

-- NNA PADECIMIENTOS (depende de nna, padecimiento)
CREATE TABLE IF NOT EXISTS public.nna_padecimientos (
    id_nna int NOT NULL,
    id_padecimiento int NOT NULL,
    fecha_diagnostico DATE,
    observaciones text,
    bajo_control BOOLEAN DEFAULT FALSE, 
    cronico BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id_nna, id_padecimiento),
    CONSTRAINT fk_nna_padecimiento FOREIGN KEY (id_nna) 
        REFERENCES public.nna(id_nna) ON DELETE CASCADE,
    CONSTRAINT fk_padecimiento_nna FOREIGN KEY (id_padecimiento) 
        REFERENCES public.padecimiento(id_padecimiento) ON DELETE CASCADE
);

-- NNA DISCAPACIDAD (depende de nna, tipo_discapacidad, grado_dependencia)
CREATE TABLE IF NOT EXISTS public.nna_discapacidad (
    id_nna_discapacidad SERIAL,
    id_nna INT NOT NULL,
    nombre_comun VARCHAR(100) NOT NULL,
    id_tipo_discapacidad INT,
    id_grado_dependencia INT,
    descripcion TEXT,
    requiere_aditamento BOOLEAN DEFAULT FALSE,
    cuenta_con_aditamento BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    CONSTRAINT fk_nna_discapacidad_nna FOREIGN KEY (id_nna) REFERENCES public.nna(id_nna) ON DELETE CASCADE,
    CONSTRAINT fk_tipo_discapacidad FOREIGN KEY (id_tipo_discapacidad) REFERENCES public.tipo_discapacidad(id_tipo_discapacidad) ON DELETE SET NULL,
    CONSTRAINT fk_grado_dependencia FOREIGN KEY (id_grado_dependencia) REFERENCES public.grado_dependencia(id_grado_dependencia) ON DELETE SET NULL,
    CONSTRAINT id_nna_discapacidad_pkey PRIMARY KEY (id_nna_discapacidad)
);

-- DOCUMENTOS NNA (depende de nna, tipo_documento_nna)
CREATE TABLE IF NOT EXISTS public.documentos_nna (
    id_documento_nna SERIAL,
    id_nna INT NOT NULL UNIQUE,
    id_documento INT,
    id_tipo_documento_nna INT NOT NULL,
    ruta_archivo VARCHAR(255),
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    CONSTRAINT fk_documentos_nna_nna FOREIGN KEY (id_nna) REFERENCES public.nna(id_nna) ON DELETE CASCADE,
    CONSTRAINT fk_documentos_nna_documento FOREIGN KEY (id_documento) REFERENCES public.documentos(id_documento) ON DELETE SET NULL,
    CONSTRAINT fk_documentos_nna_tipo FOREIGN KEY (id_tipo_documento_nna) REFERENCES public.tipo_documento_nna(id_tipo_documento_nna) ON DELETE RESTRICT,
    CONSTRAINT id_documento_nna_pkey PRIMARY KEY(id_documento_nna),
    CONSTRAINT documentos_nna_unico_tipo_por_nna UNIQUE(id_nna, id_tipo_documento_nna)
);

-- ALTER para agregar FK a documentos_nna en nna
ALTER TABLE public.nna
    ADD CONSTRAINT fk_documentos_nna FOREIGN KEY (id_documentos_nna) 
        REFERENCES public.documentos_nna(id_documento_nna) ON UPDATE CASCADE ON DELETE SET NULL;

-- ACTA NACIMIENTO (depende de documentos_nna, estado_documento)
CREATE TABLE IF NOT EXISTS public.acta_nacimiento (
    id_acta_nacimiento SERIAL,
    id_documento_nna INT NOT NULL UNIQUE,
    fecha_expedicion DATE,
    id_estado_documento INT,
    observaciones TEXT,
    CONSTRAINT fk_acta_doc_nna FOREIGN KEY (id_documento_nna) REFERENCES public.documentos_nna(id_documento_nna) ON DELETE CASCADE,
    CONSTRAINT fk_acta_estado_documento FOREIGN KEY (id_estado_documento) REFERENCES public.estado_documento(id_estado_documento) ON DELETE SET NULL,
    CONSTRAINT id_acta_nacimiento_pkey PRIMARY KEY(id_acta_nacimiento)
);

-- CARTILLA MEDICA (depende de documentos_nna, institucion_medica, estado_documento)
CREATE TABLE IF NOT EXISTS public.cartilla_medica (
    id_cartilla_medica SERIAL,
    id_documento_nna INT NOT NULL UNIQUE,
    fecha_emision DATE,
    fecha_vencimiento DATE,
    id_institucion_medica INT,
    id_estado_documento INT,
    observaciones TEXT,
    CONSTRAINT fk_cartilla_doc_nna FOREIGN KEY (id_documento_nna) REFERENCES public.documentos_nna(id_documento_nna) ON DELETE CASCADE,
    CONSTRAINT fk_cartilla_institucion FOREIGN KEY (id_institucion_medica) REFERENCES public.institucion_medica(id_institucion_medica) ON DELETE SET NULL,
    CONSTRAINT fk_cartilla_estado_documento FOREIGN KEY (id_estado_documento) REFERENCES public.estado_documento(id_estado_documento) ON DELETE SET NULL,
    CONSTRAINT id_cartilla_medica_pkey PRIMARY KEY(id_cartilla_medica)
);

-- FAMILIARES (depende de personas_expediente)
CREATE TABLE IF NOT EXISTS public.familiares (
    id_familiar SERIAL,
    id_persona_exp int NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    observaciones text,
    CONSTRAINT fk_persona_familiar FOREIGN KEY (id_persona_exp) 
        REFERENCES public.personas_expediente(id_persona_exp) ON DELETE CASCADE,
    CONSTRAINT id_familiar_pkey PRIMARY KEY(id_familiar)
);

-- TUTORES (depende de personas_expediente, parentesco, grado_negacion, grado_afectacion_emocional, telefonos, correos)
CREATE TABLE IF NOT EXISTS public.tutores (
    id_tutor SERIAL,
    id_persona_exp int NOT NULL,
    ocupacion VARCHAR(50) NOT NULL,
    es_sosten_economico BOOLEAN NOT NULL DEFAULT TRUE,
    observaciones text,
    escolaridad VARCHAR(50) NOT NULL,
    patron_migracion text,
    id_telefono INT,
    id_correo INT,
    id_parentesco int,
    id_grado_negacion int,
    id_grado_afectacion_emocional int,

    CONSTRAINT fk_telefono_tutores FOREIGN KEY (id_telefono) 
        REFERENCES public.telefonos_tutores(id_telefono) ON DELETE SET NULL,
    CONSTRAINT fk_correo_tutores FOREIGN KEY (id_correo) 
        REFERENCES public.correos_tutores(id_correo) ON DELETE SET NULL,
    CONSTRAINT fk_parenteso_tutores FOREIGN KEY (id_parentesco) 
        REFERENCES public.parentesco(id_parentesco) ON DELETE CASCADE,
    CONSTRAINT fk_grado_negacion_tutores FOREIGN KEY (id_grado_negacion) 
        REFERENCES public.grado_negacion(id_grado_negacion) ON DELETE SET NULL,
    CONSTRAINT fk_grado_afectacion_emocional_tutores FOREIGN KEY (id_grado_afectacion_emocional) 
        REFERENCES public.grado_afectacion_emocional(id_grado_afectacion_emocional) ON DELETE SET NULL,
    CONSTRAINT fk_persona_tutor FOREIGN KEY (id_persona_exp) 
        REFERENCES public.personas_expediente(id_persona_exp) ON DELETE CASCADE,
    CONSTRAINT id_tutor_pkey PRIMARY KEY(id_tutor)
);

-- HECHO VICTIMAL (depende de nna, tipo_detector)
CREATE TABLE IF NOT EXISTS public.hecho_victimal (
    id_hecho SERIAL,
    id_nna INT,
    num_reporte varchar(100) not null,
    nombre_caso varchar(100) not null,
    fecha_detencion DATE not null,
    nombre_victima_madre VARCHAR(100) NOT NULL,
    descripcion_delito text,
    narracion_sucedido text,
    id_tipo_detector int,
    id_direccion_delito int,
    CONSTRAINT fk_tipo_detector_hecho_victimal
        FOREIGN KEY (id_tipo_detector)
        REFERENCES public.tipo_detector(id_tipo_detector)
        ON UPDATE CASCADE
        ON DELETE CASCADE, 
    CONSTRAINT fk_nna_hecho_victimal 
        FOREIGN KEY(id_nna)
        REFERENCES public.nna(id_nna)
        ON DELETE RESTRICT,
    CONSTRAINT id_hecho_pkey PRIMARY KEY (id_hecho)
);

-- ===== PARTE 5: ACTORES Y SERVICIOS =====

-- PERSONAS SERVICIOS (depende de sexo)
CREATE TABLE IF NOT EXISTS public.personas_servicios (
    id_persona_servicio SERIAL,
    p_nombre VARCHAR(50) NOT NULL,
    s_nombre VARCHAR(50),
    p_apellido VARCHAR(50) NOT NULL,
    s_apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE,
    id_sexo_persona INT,
    CONSTRAINT fk_sexo_personas_servicios FOREIGN KEY (id_sexo_persona)
        REFERENCES public.sexo(id_sexo) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT id_persona_servicio_pkey PRIMARY KEY (id_persona_servicio)
);

-- COLONIAS SERVICIOS (depende de codigo_postal, municipios)
CREATE TABLE IF NOT EXISTS public.colonias_servicios (
    id_colonia_servicio SERIAL,
    nombre_colonia VARCHAR(100) NOT NULL,
    id_cp INT,
    id_municipio INT,
    CONSTRAINT fk_codigo_postal_colonias_servicios FOREIGN KEY (id_cp)
        REFERENCES public.codigo_postal(id_cp) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_municipio_colonias_servicios FOREIGN KEY (id_municipio)
        REFERENCES public.municipios(id_municipio) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT id_colonia_servicio_pkey PRIMARY KEY (id_colonia_servicio)
);

-- DOMICILIO SERVICIOS (depende de colonias_servicios)
CREATE TABLE IF NOT EXISTS public.domicilio_servicios (
    id_domicilio_servicio SERIAL,
    calle VARCHAR(100),
    num_ext VARCHAR(20),
    num_int VARCHAR(20),
    id_colonia_servicio INT,
    CONSTRAINT fk_colonia_servicios FOREIGN KEY (id_colonia_servicio)
        REFERENCES public.colonias_servicios(id_colonia_servicio) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT id_domicilio_servicio_pkey PRIMARY KEY (id_domicilio_servicio)
);

-- EMAIL SERVICIOS
CREATE TABLE IF NOT EXISTS public.email_servicios (
    id_email_servicio SERIAL,
    correo_email VARCHAR(100) NOT NULL UNIQUE,
    tipo_email VARCHAR(20) DEFAULT 'principal',
    CONSTRAINT id_email_servicio_pkey PRIMARY KEY (id_email_servicio)
);

-- TELEFONOS SERVICIOS
CREATE TABLE IF NOT EXISTS public.telefonos_servicios (
    id_telefono_servicio SERIAL,
    numero_telefono VARCHAR(20) NOT NULL UNIQUE,
    tipo_telefono VARCHAR(20) DEFAULT 'principal',
    CONSTRAINT id_telefono_servicio_pkey PRIMARY KEY (id_telefono_servicio)
);

-- REDES SOCIALES SERVICIOS (depende de red_social)
CREATE TABLE IF NOT EXISTS public.redes_sociales_servicios (
    id_red_social_servicio SERIAL,
    id_red_social INT NOT NULL,
    url_red_social VARCHAR(255) NOT NULL,
    CONSTRAINT fk_red_social_servicios FOREIGN KEY (id_red_social)
        REFERENCES public.red_social(id_red_social) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT id_red_social_servicio_pkey PRIMARY KEY (id_red_social_servicio)
);

-- ACTORES (depende de tipo_actor, sector_servicio, email_servicios, telefonos_servicios, redes_sociales_servicios, domicilio_servicios, estado_actor, personal)
CREATE TABLE IF NOT EXISTS public.actores (
    id_actor SERIAL,
    id_tipo_actor INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    nombre_corto VARCHAR(50),
    id_sector INT,
    descripcion TEXT,
    pagina_web VARCHAR(255),
    id_email_principal INT,
    id_telefono_principal INT,
    id_telefono_secundario INT,
    id_red_social_principal INT,
    horario_atencion VARCHAR(100),
    id_domicilio_servicio INT,
    referencias_ubicacion TEXT,
    id_estado_actor INT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registrado_por VARCHAR(18),
    CONSTRAINT fk_tipo_actor FOREIGN KEY (id_tipo_actor)
        REFERENCES public.tipo_actor(id_tipo_actor) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_sector_actor FOREIGN KEY (id_sector)
        REFERENCES public.sector_servicio(id_sector) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_email_principal_actor FOREIGN KEY (id_email_principal)
        REFERENCES public.email_servicios(id_email_servicio) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_telefono_principal_actor FOREIGN KEY (id_telefono_principal)
        REFERENCES public.telefonos_servicios(id_telefono_servicio) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_telefono_secundario_actor FOREIGN KEY (id_telefono_secundario)
        REFERENCES public.telefonos_servicios(id_telefono_servicio) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_red_social_principal_actor FOREIGN KEY (id_red_social_principal)
        REFERENCES public.redes_sociales_servicios(id_red_social_servicio) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_domicilio_servicio_actor FOREIGN KEY (id_domicilio_servicio)
        REFERENCES public.domicilio_servicios(id_domicilio_servicio) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_estado_actor_actor FOREIGN KEY (id_estado_actor)
        REFERENCES public.estado_actor(id_estado_actor) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_registrado_por_actor FOREIGN KEY (registrado_por)
        REFERENCES public.personal("CURP") ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT id_actor_pkey PRIMARY KEY (id_actor)
);
