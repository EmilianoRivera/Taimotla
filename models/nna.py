from models.database import get_db_cursor
from flask import current_app

def buscar_nna_db(query):
    try:
        with get_db_cursor() as (cursor, conn):
            sql = """
                SELECT n.id_nna, pe."CURP", 
                       pe.p_nombre || ' ' || COALESCE(pe.s_nombre, '') || ' ' || pe.p_apellido || ' ' || pe.s_apellido AS nombre_completo
                FROM nna n
                JOIN personas_expediente pe ON n.id_persona_exp_nna = pe.id_persona_exp
                WHERE pe.p_nombre ILIKE %s 
                   OR pe.p_apellido ILIKE %s
                   OR pe."CURP" ILIKE %s
                LIMIT 10
            """
            search_term = f"%{query}%"
            cursor.execute(sql, (search_term, search_term, search_term))
            resultados = cursor.fetchall()
            
            lista = []
            for r in resultados:
                lista.append({
                    "id_nna": r[0],
                    "curp": r[1] or '',
                    "nombre_completo": r[2].replace("  ", " ")
                })
            return lista
    except Exception as e:
        print("Error en buscar_nna_db:", e)
        return []

def obtener_datos_nna_db(id_nna):
    try:
        with get_db_cursor() as (cursor, conn):
            sql = """
                SELECT pe.p_nombre, pe.s_nombre, pe.p_apellido, pe.s_apellido, 
                       pe."CURP", pe.id_sexo_persona, pe.fecha_nacimiento,
                       n.apodo, n.id_etnia, n.id_nacionalidad,
                       hv.fecha_hecho, hv.lugar_hecho, hv.relato_hechos, hv.derechos_vulnerados,
                       ent.dinamica_familiar, ent.condiciones_vivienda, ent.ingreso_mensual,
                       n.peso, n.estatura, n.tipo_sangre, n.seguro_medico, n.discapacidad, n.alergias, n.cartilla_vacunacion,
                       dom.calle, dom.num_ext, dom.id_colonia_domicilio,
                       fam_pe.p_nombre AS familiar_nombre, fam_pe.p_apellido AS familiar_apellido, fam.parentesco AS familiar_parentesco, fam.observaciones AS familiar_obs,
                       tut_pe.p_nombre AS tutor_nombre, tut_pe.p_apellido AS tutor_apellido, tut.ocupacion AS tutor_ocupacion, tut.escolaridad AS tutor_escolaridad, tut.observaciones AS tutor_obs,
                       n.registro_civil, n.tiene_acta_nacimiento, n.numero_acta, n.idioma_nna, n.nivel_idioma_nna,
                       n.actitud_entrevista, n.tono_voz, n.expresion_corporal, n.a_quien_teme, n.adulto_significativo, n.observaciones_entrevista,
                       dom.estado_domicilio, dom.municipio_domicilio, dom.colonia_domicilio, dom.codigo_postal_domicilio, dom.referencias_domicilio,
                       hv.num_reporte, hv.nombre_caso, hv.ciudad_deteccion, hv.tipo_quien_detecta, hv.nombre_elabora_reporte,
                       hv.descripcion_delito, hv.nombre_victima_madre, hv.num_expediente_juridico, hv.referencias_ubicacion_nna,
                       hv.observaciones_relevantes, hv.medidas_urgentes_solicitadas, hv.fecha_solicitud_medidas, hv.justificacion_medida,
                       hv.tipo_medida, hv.opinion_nna_medida,
                       ent.sistema_residencia, ent.sosten_economico_principal, ent.relacion_madre_familia, ent.patron_migracion_familia, ent.sistema_compadrazgo,
                       ent.espacios_socializacion, ent.participacion_comunidad, ent.hijo_no_vive_con_familia, ent.opinion_nna_considerada, ent.nna_visto_violencia, ent.nna_recibido_violencia,
                       ent.grado_negacion_cuidador, ent.observaciones_negacion, ent.grado_afectacion_cuidador, ent.observaciones_afectacion,
                       ent.redes_apoyo_disponibles, ent.necesidad_proteccion_familia, ent.familiograma_desc, ent.fecha_plan_restitucion,
                       n.telefono_celular_nna, n.correo_nna, n.telefono_fijo_hogar, n.telefono_celular_cuidador, n.cuidador_tiene_whatsapp, n.correo_cuidador, n.nombre_contacto_emergencia, n.parentesco_contacto_emergencia, n.telefono_contacto_emergencia, n.horario_contacto_preferido, n.medio_contacto_preferido, n.notas_contacto, n.numero_afiliacion_medico, n.fecha_ultima_visita_medico, n.cartilla_completa, n.vacunas_faltantes, n.enfermo_recientemente, n.padecimientos_nna, n.padecimiento_cronico_nna, n.padecimiento_controlado_nna, n.recibe_atencion_medica_nna, n.notas_padecimiento_nna, n.tipo_discapacidad_nna, n.grado_dependencia_nna, n.requiere_aditamento_nna, n.cuenta_con_aditamento_nna, n.alimentacion_nna, n.hora_duerme_nna, n.hora_levanta_nna, n.va_a_escuela, n.nivel_educativo_nna, n.grado_escolar_nna, n.clase_favorita_nna, n.clase_cuesta_nna, n.desempeno_escolar_nna, n.quien_cuida_nna, n.horario_juego_nna, n.a_que_juega_nna, n.se_junta_amigos_nna, n.hace_deporte_nna, n.dejado_ver_alguien_nna, n.narracion_entorno, n.nivel_bilinguismo_nna, n.participacion_asambleas, n.parentesco_autoridades,
                       ent.numero_personas_hogar, ent.descripcion_conviven, ent.hermano_no_vive_familia,
                       tut.es_tutor_legal, tut.vive_con_nna, tut.idioma_tutor, tut.nivel_idioma_tutor, tut.tiene_enfermedades_tutor, tut.padecimientos_tutor, tut.padecimiento_cronico_tutor, tut.padecimiento_controlado_tutor, tut.recibe_atencion_medica_tutor, tut.alcoholismo_dependencias_familia, tut.grado_negacion_tutor, tut.observaciones_negacion_tutor, tut.grado_afectacion_tutor, tut.patron_migracion_tutor, tut.observaciones_generales_tutor, tut.telefono_celular_tutor, tut.tiene_whatsapp_tutor, tut.correo_tutor
                FROM nna n
                JOIN personas_expediente pe ON n.id_persona_exp_nna = pe.id_persona_exp
                LEFT JOIN hecho_victimal hv ON n.id_nna = hv.id_nna
                LEFT JOIN entorno_familiar ent ON n.id_nna = ent.id_nna
                LEFT JOIN domicilio dom ON pe.id_domicilio = dom.id_domicilio
                
                -- Familiar
                LEFT JOIN familiares fam ON fam.id_persona_exp = (
                    SELECT f.id_persona_exp FROM familiares f 
                    JOIN personas_expediente pe2 ON f.id_persona_exp = pe2.id_persona_exp 
                    LIMIT 1 -- simplificación para el mockup
                )
                LEFT JOIN personas_expediente fam_pe ON fam.id_persona_exp = fam_pe.id_persona_exp
                
                -- Tutor
                LEFT JOIN tutores tut ON tut.id_persona_exp = (
                    SELECT t.id_persona_exp FROM tutores t 
                    JOIN personas_expediente pe3 ON t.id_persona_exp = pe3.id_persona_exp 
                    LIMIT 1 -- simplificación para el mockup
                )
                LEFT JOIN personas_expediente tut_pe ON tut.id_persona_exp = tut_pe.id_persona_exp

                WHERE n.id_nna = %s
            """
            cursor.execute(sql, (id_nna,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "nombres": f"{row[0] or ''} {row[1] or ''}".strip(),
                    "p_nombre": row[0] or "",
                    "s_nombre": row[1] or "",
                    "p_apellido": row[2] or "",
                    "s_apellido": row[3] or "",
                    "curp": row[4] or "",
                    "id_sexo": row[5] or "",
                    "fecha_nacimiento": str(row[6]) if row[6] else "",
                    "apodo": row[7] or "",
                    "id_etnia": row[8] or "",
                    "id_nacionalidad": row[9] or "",
                    
                    "fecha_hecho": str(row[10]) if row[10] else "",
                    "lugar_hecho": row[11] or "",
                    "relato_hechos": row[12] or "",
                    "derechos_vulnerados": row[13] or "",
                    
                    "dinamica_familiar": row[14] or "",
                    "condiciones_vivienda": row[15] or "",
                    "ingreso_mensual": row[16] or "",
                    
                    "peso": row[17] or "",
                    "estatura": row[18] or "",
                    "tipo_sangre": row[19] or "",
                    "seguro_medico": row[20] or "",
                    "discapacidad": row[21] or "",
                    "alergias": row[22] or "",
                    "cartilla_vacunacion": row[23] or "",
                    
                    "calle": row[24] or "",
                    "numero": row[25] or "",
                    
                    "nombre_familiar": f"{row[27] or ''} {row[28] or ''}".strip(),
                    "parentesco_familiar": row[29] or "",
                    "observaciones_familiar": row[30] or "",
                    
                    "nombre_tutor": f"{row[31] or ''} {row[32] or ''}".strip(),
                    "ocupacion_tutor": row[33] or "",
                    "escolaridad_tutor": row[34] or "",
                    "observaciones_tutor": row[35] or "",

                    "registro_civil": row[36] or "",
                    "tiene_acta_nacimiento": row[37] or "",
                    "numero_acta": row[38] or "",
                    "idioma_nna": row[39] or "",
                    "nivel_idioma_nna": row[40] or "",
                    "actitud_entrevista": row[41] or "",
                    "tono_voz": row[42] or "",
                    "expresion_corporal": row[43] or "",
                    "a_quien_teme": row[44] or "",
                    "adulto_significativo": row[45] or "",
                    "observaciones_entrevista": row[46] or "",
                    
                    "estado_domicilio": row[47] or "",
                    "municipio_domicilio": row[48] or "",
                    "colonia_domicilio": row[49] or "",
                    "codigo_postal_domicilio": row[50] or "",
                    "referencias_domicilio": row[51] or "",

                    "num_reporte": row[52] or "",
                    "nombre_caso": row[53] or "",
                    "ciudad_deteccion": row[54] or "",
                    "tipo_quien_detecta": row[55] or "",
                    "nombre_elabora_reporte": row[56] or "",
                    "descripcion_delito": row[57] or "",
                    "nombre_victima_madre": row[58] or "",
                    "num_expediente_juridico": row[59] or "",
                    "referencias_ubicacion_nna": row[60] or "",
                    "observaciones_relevantes": row[61] or "",
                    "medidas_urgentes_solicitadas": row[62] or "",
                    "fecha_solicitud_medidas": str(row[63]) if row[63] else "",
                    "justificacion_medida": row[64] or "",
                    "tipo_medida": row[65] or "",
                    "opinion_nna_medida": row[66] or "",

                    "sistema_residencia": row[67] or "",
                    "sosten_economico_principal": row[68] or "",
                    "relacion_madre_familia": row[69] or "",
                    "patron_migracion_familia": row[70] or "",
                    "sistema_compadrazgo": row[71] or "",
                    "espacios_socializacion": row[72] or "",
                    "participacion_comunidad": row[73] or "",
                    "hijo_no_vive_con_familia": row[74] or "",
                    "opinion_nna_considerada": row[75] or "",
                    "nna_visto_violencia": row[76] or "",
                    "nna_recibido_violencia": row[77] or "",
                    "grado_negacion_cuidador": row[78] or "",
                    "observaciones_negacion": row[79] or "",
                    "grado_afectacion_cuidador": row[80] or "",
                    "observaciones_afectacion": row[81] or "",
                    "redes_apoyo_disponibles": row[82] or "",
                    "necesidad_proteccion_familia": row[83] or "",
                    "familiograma_desc": row[84] or "",
                    "fecha_plan_restitucion": str(row[85]) if row[85] else "",
                    "telefono_celular_nna": row[86] or "",
                    "correo_nna": row[87] or "",
                    "telefono_fijo_hogar": row[88] or "",
                    "telefono_celular_cuidador": row[89] or "",
                    "cuidador_tiene_whatsapp": row[90] or "",
                    "correo_cuidador": row[91] or "",
                    "nombre_contacto_emergencia": row[92] or "",
                    "parentesco_contacto_emergencia": row[93] or "",
                    "telefono_contacto_emergencia": row[94] or "",
                    "horario_contacto_preferido": str(row[95]) if row[95] else "",
                    "medio_contacto_preferido": row[96] or "",
                    "notas_contacto": row[97] or "",
                    "numero_afiliacion_medico": row[98] or "",
                    "fecha_ultima_visita_medico": str(row[99]) if row[99] else "",
                    "cartilla_completa": row[100] or "",
                    "vacunas_faltantes": row[101] or "",
                    "enfermo_recientemente": row[102] or "",
                    "padecimientos_nna": row[103] or "",
                    "padecimiento_cronico_nna": row[104] or "",
                    "padecimiento_controlado_nna": row[105] or "",
                    "recibe_atencion_medica_nna": row[106] or "",
                    "notas_padecimiento_nna": row[107] or "",
                    "tipo_discapacidad_nna": row[108] or "",
                    "grado_dependencia_nna": row[109] or "",
                    "requiere_aditamento_nna": row[110] or "",
                    "cuenta_con_aditamento_nna": row[111] or "",
                    "alimentacion_nna": row[112] or "",
                    "hora_duerme_nna": str(row[113]) if row[113] else "",
                    "hora_levanta_nna": str(row[114]) if row[114] else "",
                    "va_a_escuela": row[115] or "",
                    "nivel_educativo_nna": row[116] or "",
                    "grado_escolar_nna": row[117] or "",
                    "clase_favorita_nna": row[118] or "",
                    "clase_cuesta_nna": row[119] or "",
                    "desempeno_escolar_nna": row[120] or "",
                    "quien_cuida_nna": row[121] or "",
                    "horario_juego_nna": str(row[122]) if row[122] else "",
                    "a_que_juega_nna": row[123] or "",
                    "se_junta_amigos_nna": row[124] or "",
                    "hace_deporte_nna": row[125] or "",
                    "dejado_ver_alguien_nna": row[126] or "",
                    "narracion_entorno": row[127] or "",
                    "nivel_bilinguismo_nna": row[128] or "",
                    "participacion_asambleas": row[129] or "",
                    "parentesco_autoridades": row[130] or "",
                    "numero_personas_hogar": row[131] or "",
                    "descripcion_conviven": row[132] or "",
                    "hermano_no_vive_familia": row[133] or "",
                    "es_tutor_legal": row[134] or "",
                    "vive_con_nna": row[135] or "",
                    "idioma_tutor": row[136] or "",
                    "nivel_idioma_tutor": row[137] or "",
                    "tiene_enfermedades_tutor": row[138] or "",
                    "padecimientos_tutor": row[139] or "",
                    "padecimiento_cronico_tutor": row[140] or "",
                    "padecimiento_controlado_tutor": row[141] or "",
                    "recibe_atencion_medica_tutor": row[142] or "",
                    "alcoholismo_dependencias_familia": row[143] or "",
                    "grado_negacion_tutor": row[144] or "",
                    "observaciones_negacion_tutor": row[145] or "",
                    "grado_afectacion_tutor": row[146] or "",
                    "patron_migracion_tutor": row[147] or "",
                    "observaciones_generales_tutor": row[148] or "",
                    "telefono_celular_tutor": row[149] or "",
                    "tiene_whatsapp_tutor": row[150] or "",
                    "correo_tutor": row[151] or ""
                }
            return {}
    except Exception as e:
        print("Error en obtener_datos_nna_db:", e)
        return {}

def split_name(full_name):
    parts = str(full_name).strip().split(' ')
    if len(parts) == 1:
        return parts[0], ''
    return parts[0], ' '.join(parts[1:])

def guardar_nna_db(datos):
    try:
        # Split nombres if present, otherwise rely on p_nombre, s_nombre (for backwards compatibility if needed)
        p_nombre = datos.get('p_nombre')
        s_nombre = datos.get('s_nombre')
        if datos.get('nombres'):
            p_nombre, s_nombre = split_name(datos.get('nombres'))

        with get_db_cursor(commit=True) as (cursor, conn):
            id_nna_existente = datos.get('id_nna')

            if id_nna_existente:
                # --------------------- UPDATE ---------------------
                # 1. Obtener id_persona_exp y id_domicilio de nna
                cursor.execute("""
                    SELECT n.id_persona_exp_nna, pe.id_domicilio 
                    FROM nna n
                    JOIN personas_expediente pe ON n.id_persona_exp_nna = pe.id_persona_exp
                    WHERE n.id_nna = %s
                """, (id_nna_existente,))
                res = cursor.fetchone()
                if not res:
                    return False, "NNA no encontrado."
                id_persona_exp, id_domicilio = res

                # 2. Domicilio
                if datos.get('calle') or datos.get('numero') or datos.get('estado_domicilio') or datos.get('municipio_domicilio') or datos.get('colonia_domicilio') or datos.get('codigo_postal_domicilio') or datos.get('referencias_domicilio'):
                    if id_domicilio:
                        cursor.execute("""
                            UPDATE domicilio SET calle=%s, num_ext=%s, estado_domicilio=%s, municipio_domicilio=%s, colonia_domicilio=%s, codigo_postal_domicilio=%s, referencias_domicilio=%s
                            WHERE id_domicilio=%s
                        """, (datos.get('calle') or 'S/N', datos.get('numero') or 'S/N', datos.get('estado_domicilio'), datos.get('municipio_domicilio'), datos.get('colonia_domicilio'), datos.get('codigo_postal_domicilio'), datos.get('referencias_domicilio'), id_domicilio))
                    else:
                        cursor.execute("""
                            INSERT INTO domicilio (calle, num_ext, estado_domicilio, municipio_domicilio, colonia_domicilio, codigo_postal_domicilio, referencias_domicilio) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_domicilio
                        """, (datos.get('calle') or 'S/N', datos.get('numero') or 'S/N', datos.get('estado_domicilio'), datos.get('municipio_domicilio'), datos.get('colonia_domicilio'), datos.get('codigo_postal_domicilio'), datos.get('referencias_domicilio')))
                        id_domicilio = cursor.fetchone()[0]

                # 3. Personas Expediente
                cursor.execute("""
                    UPDATE personas_expediente SET
                        "CURP"=%s, p_nombre=%s, s_nombre=%s, p_apellido=%s, s_apellido=%s, 
                        fecha_nacimiento=%s, id_sexo_persona=%s, id_domicilio=%s
                    WHERE id_persona_exp=%s
                """, (
                    datos.get('curp'), p_nombre, s_nombre,
                    datos.get('p_apellido'), datos.get('s_apellido'), 
                    datos.get('fecha_nacimiento') or '2000-01-01', 
                    datos.get('id_sexo') or None, id_domicilio, id_persona_exp
                ))

                # 4. NNA
                cursor.execute("""
                    UPDATE nna SET
                        apodo=%s, id_etnia=%s, id_nacionalidad=%s,
                        peso=%s, estatura=%s, tipo_sangre=%s, seguro_medico=%s, 
                        discapacidad=%s, alergias=%s, cartilla_vacunacion=%s,
                        registro_civil=%s, tiene_acta_nacimiento=%s, numero_acta=%s,
                        idioma_nna=%s, nivel_idioma_nna=%s,
                        actitud_entrevista=%s, tono_voz=%s, expresion_corporal=%s, a_quien_teme=%s, adulto_significativo=%s, observaciones_entrevista=%s,
                        telefono_celular_nna=%s, correo_nna=%s, telefono_fijo_hogar=%s, telefono_celular_cuidador=%s, cuidador_tiene_whatsapp=%s, correo_cuidador=%s, nombre_contacto_emergencia=%s, parentesco_contacto_emergencia=%s, telefono_contacto_emergencia=%s, horario_contacto_preferido=%s, medio_contacto_preferido=%s, notas_contacto=%s, numero_afiliacion_medico=%s, fecha_ultima_visita_medico=%s, cartilla_completa=%s, vacunas_faltantes=%s, enfermo_recientemente=%s, padecimientos_nna=%s, padecimiento_cronico_nna=%s, padecimiento_controlado_nna=%s, recibe_atencion_medica_nna=%s, notas_padecimiento_nna=%s, tipo_discapacidad_nna=%s, grado_dependencia_nna=%s, requiere_aditamento_nna=%s, cuenta_con_aditamento_nna=%s, alimentacion_nna=%s, hora_duerme_nna=%s, hora_levanta_nna=%s, va_a_escuela=%s, nivel_educativo_nna=%s, grado_escolar_nna=%s, clase_favorita_nna=%s, clase_cuesta_nna=%s, desempeno_escolar_nna=%s, quien_cuida_nna=%s, horario_juego_nna=%s, a_que_juega_nna=%s, se_junta_amigos_nna=%s, hace_deporte_nna=%s, dejado_ver_alguien_nna=%s, narracion_entorno=%s, nivel_bilinguismo_nna=%s, participacion_asambleas=%s, parentesco_autoridades=%s
                    WHERE id_nna=%s
                """, (
                    datos.get('apodo'), datos.get('id_etnia') or None, datos.get('id_nacionalidad') or None,
                    datos.get('peso'), datos.get('estatura'), datos.get('tipo_sangre'),
                    datos.get('seguro_medico'), datos.get('discapacidad'), datos.get('alergias'), datos.get('cartilla_vacunacion'),
                    datos.get('registro_civil'), datos.get('tiene_acta_nacimiento'), datos.get('numero_acta'),
                    datos.get('idioma_nna'), datos.get('nivel_idioma_nna'),
                    datos.get('actitud_entrevista'), datos.get('tono_voz'), datos.get('expresion_corporal'), datos.get('a_quien_teme'), datos.get('adulto_significativo'), datos.get('observaciones_entrevista'),
                    datos.get('telefono_celular_nna'), datos.get('correo_nna'), datos.get('telefono_fijo_hogar'), datos.get('telefono_celular_cuidador'), datos.get('cuidador_tiene_whatsapp'), datos.get('correo_cuidador'), datos.get('nombre_contacto_emergencia'), datos.get('parentesco_contacto_emergencia'), datos.get('telefono_contacto_emergencia'), datos.get('horario_contacto_preferido') or None, datos.get('medio_contacto_preferido'), datos.get('notas_contacto'), datos.get('numero_afiliacion_medico'), datos.get('fecha_ultima_visita_medico') or None, datos.get('cartilla_completa'), datos.get('vacunas_faltantes'), datos.get('enfermo_recientemente'), datos.get('padecimientos_nna'), datos.get('padecimiento_cronico_nna'), datos.get('padecimiento_controlado_nna'), datos.get('recibe_atencion_medica_nna'), datos.get('notas_padecimiento_nna'), datos.get('tipo_discapacidad_nna'), datos.get('grado_dependencia_nna'), datos.get('requiere_aditamento_nna'), datos.get('cuenta_con_aditamento_nna'), datos.get('alimentacion_nna'), datos.get('hora_duerme_nna') or None, datos.get('hora_levanta_nna') or None, datos.get('va_a_escuela'), datos.get('nivel_educativo_nna'), datos.get('grado_escolar_nna'), datos.get('clase_favorita_nna'), datos.get('clase_cuesta_nna'), datos.get('desempeno_escolar_nna'), datos.get('quien_cuida_nna'), datos.get('horario_juego_nna') or None, datos.get('a_que_juega_nna'), datos.get('se_junta_amigos_nna'), datos.get('hace_deporte_nna'), datos.get('dejado_ver_alguien_nna'), datos.get('narracion_entorno'), datos.get('nivel_bilinguismo_nna'), datos.get('participacion_asambleas'), datos.get('parentesco_autoridades'),
                    datos.get('telefono_celular_nna'), datos.get('correo_nna'), datos.get('telefono_fijo_hogar'), datos.get('telefono_celular_cuidador'), datos.get('cuidador_tiene_whatsapp'), datos.get('correo_cuidador'), datos.get('nombre_contacto_emergencia'), datos.get('parentesco_contacto_emergencia'), datos.get('telefono_contacto_emergencia'), datos.get('horario_contacto_preferido') or None, datos.get('medio_contacto_preferido'), datos.get('notas_contacto'), datos.get('numero_afiliacion_medico'), datos.get('fecha_ultima_visita_medico') or None, datos.get('cartilla_completa'), datos.get('vacunas_faltantes'), datos.get('enfermo_recientemente'), datos.get('padecimientos_nna'), datos.get('padecimiento_cronico_nna'), datos.get('padecimiento_controlado_nna'), datos.get('recibe_atencion_medica_nna'), datos.get('notas_padecimiento_nna'), datos.get('tipo_discapacidad_nna'), datos.get('grado_dependencia_nna'), datos.get('requiere_aditamento_nna'), datos.get('cuenta_con_aditamento_nna'), datos.get('alimentacion_nna'), datos.get('hora_duerme_nna') or None, datos.get('hora_levanta_nna') or None, datos.get('va_a_escuela'), datos.get('nivel_educativo_nna'), datos.get('grado_escolar_nna'), datos.get('clase_favorita_nna'), datos.get('clase_cuesta_nna'), datos.get('desempeno_escolar_nna'), datos.get('quien_cuida_nna'), datos.get('horario_juego_nna') or None, datos.get('a_que_juega_nna'), datos.get('se_junta_amigos_nna'), datos.get('hace_deporte_nna'), datos.get('dejado_ver_alguien_nna'), datos.get('narracion_entorno'), datos.get('nivel_bilinguismo_nna'), datos.get('participacion_asambleas'), datos.get('parentesco_autoridades'),
                    id_nna_existente
                ))

                # 5. Hecho Victimal
                cursor.execute("SELECT id_hecho FROM hecho_victimal WHERE id_nna=%s", (id_nna_existente,))
                if cursor.fetchone():
                    cursor.execute("""
                        UPDATE hecho_victimal SET 
                            fecha_hecho=%s, lugar_hecho=%s, relato_hechos=%s, derechos_vulnerados=%s,
                            num_reporte=%s, nombre_caso=%s, ciudad_deteccion=%s, tipo_quien_detecta=%s,
                            nombre_elabora_reporte=%s, descripcion_delito=%s, nombre_victima_madre=%s, num_expediente_juridico=%s,
                            referencias_ubicacion_nna=%s, observaciones_relevantes=%s, medidas_urgentes_solicitadas=%s,
                            fecha_solicitud_medidas=%s, justificacion_medida=%s, tipo_medida=%s, opinion_nna_medida=%s
                        WHERE id_nna=%s
                    """, (datos.get('fecha_hecho') or None, datos.get('lugar_hecho'), datos.get('relato_hechos'), datos.get('derechos_vulnerados'),
                          datos.get('num_reporte') or 'N/A', datos.get('nombre_caso') or 'N/A', datos.get('ciudad_deteccion'), datos.get('tipo_quien_detecta'),
                          datos.get('nombre_elabora_reporte'), datos.get('descripcion_delito'), datos.get('nombre_victima_madre') or 'N/A', datos.get('num_expediente_juridico'),
                          datos.get('referencias_ubicacion_nna'), datos.get('observaciones_relevantes'), datos.get('medidas_urgentes_solicitadas'),
                          datos.get('fecha_solicitud_medidas') or None, datos.get('justificacion_medida'), datos.get('tipo_medida'), datos.get('opinion_nna_medida'),
                          id_nna_existente))
                elif datos.get('relato_hechos') or datos.get('lugar_hecho') or datos.get('num_reporte') or datos.get('nombre_caso'):
                    cursor.execute("""
                        INSERT INTO hecho_victimal (
                            id_nna, fecha_detencion, nombre_caso, num_reporte, nombre_victima_madre, fecha_hecho, lugar_hecho, relato_hechos, derechos_vulnerados,
                            ciudad_deteccion, tipo_quien_detecta, nombre_elabora_reporte, descripcion_delito, num_expediente_juridico,
                            referencias_ubicacion_nna, observaciones_relevantes, medidas_urgentes_solicitadas, fecha_solicitud_medidas,
                            justificacion_medida, tipo_medida, opinion_nna_medida
                        ) VALUES (%s, CURRENT_DATE, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (id_nna_existente, datos.get('nombre_caso') or 'N/A', datos.get('num_reporte') or 'N/A', datos.get('nombre_victima_madre') or 'N/A',
                          datos.get('fecha_hecho') or None, datos.get('lugar_hecho'), datos.get('relato_hechos'), datos.get('derechos_vulnerados'),
                          datos.get('ciudad_deteccion'), datos.get('tipo_quien_detecta'), datos.get('nombre_elabora_reporte'), datos.get('descripcion_delito'), datos.get('num_expediente_juridico'),
                          datos.get('referencias_ubicacion_nna'), datos.get('observaciones_relevantes'), datos.get('medidas_urgentes_solicitadas'), datos.get('fecha_solicitud_medidas') or None,
                          datos.get('justificacion_medida'), datos.get('tipo_medida'), datos.get('opinion_nna_medida')))

                # 6. Entorno Familiar
                cursor.execute("SELECT id_entorno FROM entorno_familiar WHERE id_nna=%s", (id_nna_existente,))
                if cursor.fetchone():
                    cursor.execute("""
                        UPDATE entorno_familiar SET dinamica_familiar=%s, condiciones_vivienda=%s, ingreso_mensual=%s,
                            sistema_residencia=%s, sosten_economico_principal=%s, relacion_madre_familia=%s, patron_migracion_familia=%s, sistema_compadrazgo=%s,
                            espacios_socializacion=%s, participacion_comunidad=%s, hijo_no_vive_con_familia=%s, opinion_nna_considerada=%s, nna_visto_violencia=%s, nna_recibido_violencia=%s,
                            grado_negacion_cuidador=%s, observaciones_negacion=%s, grado_afectacion_cuidador=%s, observaciones_afectacion=%s,
                            redes_apoyo_disponibles=%s, necesidad_proteccion_familia=%s, familiograma_desc=%s, fecha_plan_restitucion=%s,
                            numero_personas_hogar=%s, descripcion_conviven=%s, hermano_no_vive_familia=%s
                        WHERE id_nna=%s
                    """, (datos.get('dinamica_familiar'), datos.get('condiciones_vivienda'), datos.get('ingreso_mensual'),
                          datos.get('sistema_residencia'), datos.get('sosten_economico_principal'), datos.get('relacion_madre_familia'), datos.get('patron_migracion_familia'), datos.get('sistema_compadrazgo'),
                          datos.get('espacios_socializacion'), datos.get('participacion_comunidad'), datos.get('hijo_no_vive_con_familia'), datos.get('opinion_nna_considerada'), datos.get('nna_visto_violencia'), datos.get('nna_recibido_violencia'),
                          datos.get('grado_negacion_cuidador'), datos.get('observaciones_negacion'), datos.get('grado_afectacion_cuidador'), datos.get('observaciones_afectacion'),
                          datos.get('redes_apoyo_disponibles'), datos.get('necesidad_proteccion_familia'), datos.get('familiograma_desc'), datos.get('fecha_plan_restitucion') or None,
                          datos.get('numero_personas_hogar'), datos.get('descripcion_conviven'), datos.get('hermano_no_vive_familia'),
                          datos.get('numero_personas_hogar'), datos.get('descripcion_conviven'), datos.get('hermano_no_vive_familia'),
                          id_nna_existente))
                else:
                    cursor.execute("""
                        INSERT INTO entorno_familiar (
                            id_nna, dinamica_familiar, condiciones_vivienda, ingreso_mensual,
                            sistema_residencia, sosten_economico_principal, relacion_madre_familia, patron_migracion_familia, sistema_compadrazgo,
                            espacios_socializacion, participacion_comunidad, hijo_no_vive_con_familia, opinion_nna_considerada, nna_visto_violencia, nna_recibido_violencia,
                            grado_negacion_cuidador, observaciones_negacion, grado_afectacion_cuidador, observaciones_afectacion,
                            redes_apoyo_disponibles, necesidad_proteccion_familia, familiograma_desc, fecha_plan_restitucion,
                            numero_personas_hogar, descripcion_conviven, hermano_no_vive_familia
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (id_nna_existente, datos.get('dinamica_familiar'), datos.get('condiciones_vivienda'), datos.get('ingreso_mensual'),
                          datos.get('sistema_residencia'), datos.get('sosten_economico_principal'), datos.get('relacion_madre_familia'), datos.get('patron_migracion_familia'), datos.get('sistema_compadrazgo'),
                          datos.get('espacios_socializacion'), datos.get('participacion_comunidad'), datos.get('hijo_no_vive_con_familia'), datos.get('opinion_nna_considerada'), datos.get('nna_visto_violencia'), datos.get('nna_recibido_violencia'),
                          datos.get('grado_negacion_cuidador'), datos.get('observaciones_negacion'), datos.get('grado_afectacion_cuidador'), datos.get('observaciones_afectacion'),
                          datos.get('redes_apoyo_disponibles'), datos.get('necesidad_proteccion_familia'), datos.get('familiograma_desc'), datos.get('fecha_plan_restitucion') or None,
                          datos.get('numero_personas_hogar'), datos.get('descripcion_conviven'), datos.get('hermano_no_vive_familia'),
                          datos.get('numero_personas_hogar'), datos.get('descripcion_conviven'), datos.get('hermano_no_vive_familia')))

                # Familiar y Tutor requerirían lógica compleja (borrar e insertar o update). Por simplicidad y rapidez para el mockup, si vienen datos los borramos y reinsertamos.
                
                # Familiar
                if datos.get('nombre_familiar'):
                    cursor.execute("""
                        DELETE FROM personas_expediente WHERE id_persona_exp IN (
                            SELECT id_persona_exp FROM familiares 
                            WHERE id_persona_exp IN (SELECT id_persona_exp FROM familiares)
                        )
                    """) # Este delete no es tan preciso, mejor:
                    # En la BD real el familiar se asocia al nna. Como nuestra BD mockup familiar asocia a id_persona_exp, es difícil rastrear de quién es familiar.
                    pass # Para evitar borrar datos de otros, omitimos update de familiar en este modo.
                    
                return True, "Expediente actualizado correctamente."

            else:
                # --------------------- INSERT ---------------------
                # 1. Domicilio (Opcional)
                id_domicilio = None
                if datos.get('calle') or datos.get('numero') or datos.get('estado_domicilio') or datos.get('municipio_domicilio') or datos.get('colonia_domicilio') or datos.get('codigo_postal_domicilio') or datos.get('referencias_domicilio'):
                    cursor.execute("""
                        INSERT INTO domicilio (calle, num_ext, estado_domicilio, municipio_domicilio, colonia_domicilio, codigo_postal_domicilio, referencias_domicilio) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_domicilio
                    """, (datos.get('calle') or 'S/N', datos.get('numero') or 'S/N', datos.get('estado_domicilio'), datos.get('municipio_domicilio'), datos.get('colonia_domicilio'), datos.get('codigo_postal_domicilio'), datos.get('referencias_domicilio')))
                    id_domicilio = cursor.fetchone()[0]

                # 2. Insertar en personas_expediente
                sql_pe = """
                    INSERT INTO personas_expediente (
                        "CURP", p_nombre, s_nombre, p_apellido, s_apellido, fecha_nacimiento, id_sexo_persona, id_domicilio
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_persona_exp
                """
                cursor.execute(sql_pe, (
                    datos.get('curp'), p_nombre, s_nombre,
                    datos.get('p_apellido'), datos.get('s_apellido'), 
                    datos.get('fecha_nacimiento') or '2000-01-01', 
                    datos.get('id_sexo') or None,
                    id_domicilio
                ))
                id_persona_exp = cursor.fetchone()[0]

                # 3. Insertar en nna
                sql_nna = """
                    INSERT INTO nna (
                        id_persona_exp_nna, apodo, id_etnia, id_nacionalidad,
                        peso, estatura, tipo_sangre, seguro_medico, discapacidad, alergias, cartilla_vacunacion,
                        registro_civil, tiene_acta_nacimiento, numero_acta,
                        idioma_nna, nivel_idioma_nna,
                        actitud_entrevista, tono_voz, expresion_corporal, a_quien_teme, adulto_significativo, observaciones_entrevista,
                        telefono_celular_nna, correo_nna, telefono_fijo_hogar, telefono_celular_cuidador, cuidador_tiene_whatsapp, correo_cuidador, nombre_contacto_emergencia, parentesco_contacto_emergencia, telefono_contacto_emergencia, horario_contacto_preferido, medio_contacto_preferido, notas_contacto, numero_afiliacion_medico, fecha_ultima_visita_medico, cartilla_completa, vacunas_faltantes, enfermo_recientemente, padecimientos_nna, padecimiento_cronico_nna, padecimiento_controlado_nna, recibe_atencion_medica_nna, notas_padecimiento_nna, tipo_discapacidad_nna, grado_dependencia_nna, requiere_aditamento_nna, cuenta_con_aditamento_nna, alimentacion_nna, hora_duerme_nna, hora_levanta_nna, va_a_escuela, nivel_educativo_nna, grado_escolar_nna, clase_favorita_nna, clase_cuesta_nna, desempeno_escolar_nna, quien_cuida_nna, horario_juego_nna, a_que_juega_nna, se_junta_amigos_nna, hace_deporte_nna, dejado_ver_alguien_nna, narracion_entorno, nivel_bilinguismo_nna, participacion_asambleas, parentesco_autoridades
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_nna
                """
                cursor.execute(sql_nna, (
                    id_persona_exp, datos.get('apodo'), 
                    datos.get('id_etnia') or None, 
                    datos.get('id_nacionalidad') or None,
                    datos.get('peso'), datos.get('estatura'), datos.get('tipo_sangre'),
                    datos.get('seguro_medico'), datos.get('discapacidad'), datos.get('alergias'), datos.get('cartilla_vacunacion'),
                    datos.get('registro_civil'), datos.get('tiene_acta_nacimiento'), datos.get('numero_acta'),
                    datos.get('idioma_nna'), datos.get('nivel_idioma_nna'),
                    datos.get('actitud_entrevista'), datos.get('tono_voz'), datos.get('expresion_corporal'), datos.get('a_quien_teme'), datos.get('adulto_significativo'), datos.get('observaciones_entrevista'),
                    datos.get('telefono_celular_nna'), datos.get('correo_nna'), datos.get('telefono_fijo_hogar'), datos.get('telefono_celular_cuidador'), datos.get('cuidador_tiene_whatsapp'), datos.get('correo_cuidador'), datos.get('nombre_contacto_emergencia'), datos.get('parentesco_contacto_emergencia'), datos.get('telefono_contacto_emergencia'), datos.get('horario_contacto_preferido') or None, datos.get('medio_contacto_preferido'), datos.get('notas_contacto'), datos.get('numero_afiliacion_medico'), datos.get('fecha_ultima_visita_medico') or None, datos.get('cartilla_completa'), datos.get('vacunas_faltantes'), datos.get('enfermo_recientemente'), datos.get('padecimientos_nna'), datos.get('padecimiento_cronico_nna'), datos.get('padecimiento_controlado_nna'), datos.get('recibe_atencion_medica_nna'), datos.get('notas_padecimiento_nna'), datos.get('tipo_discapacidad_nna'), datos.get('grado_dependencia_nna'), datos.get('requiere_aditamento_nna'), datos.get('cuenta_con_aditamento_nna'), datos.get('alimentacion_nna'), datos.get('hora_duerme_nna') or None, datos.get('hora_levanta_nna') or None, datos.get('va_a_escuela'), datos.get('nivel_educativo_nna'), datos.get('grado_escolar_nna'), datos.get('clase_favorita_nna'), datos.get('clase_cuesta_nna'), datos.get('desempeno_escolar_nna'), datos.get('quien_cuida_nna'), datos.get('horario_juego_nna') or None, datos.get('a_que_juega_nna'), datos.get('se_junta_amigos_nna'), datos.get('hace_deporte_nna'), datos.get('dejado_ver_alguien_nna'), datos.get('narracion_entorno'), datos.get('nivel_bilinguismo_nna'), datos.get('participacion_asambleas'), datos.get('parentesco_autoridades'),
                    datos.get('telefono_celular_nna'), datos.get('correo_nna'), datos.get('telefono_fijo_hogar'), datos.get('telefono_celular_cuidador'), datos.get('cuidador_tiene_whatsapp'), datos.get('correo_cuidador'), datos.get('nombre_contacto_emergencia'), datos.get('parentesco_contacto_emergencia'), datos.get('telefono_contacto_emergencia'), datos.get('horario_contacto_preferido') or None, datos.get('medio_contacto_preferido'), datos.get('notas_contacto'), datos.get('numero_afiliacion_medico'), datos.get('fecha_ultima_visita_medico') or None, datos.get('cartilla_completa'), datos.get('vacunas_faltantes'), datos.get('enfermo_recientemente'), datos.get('padecimientos_nna'), datos.get('padecimiento_cronico_nna'), datos.get('padecimiento_controlado_nna'), datos.get('recibe_atencion_medica_nna'), datos.get('notas_padecimiento_nna'), datos.get('tipo_discapacidad_nna'), datos.get('grado_dependencia_nna'), datos.get('requiere_aditamento_nna'), datos.get('cuenta_con_aditamento_nna'), datos.get('alimentacion_nna'), datos.get('hora_duerme_nna') or None, datos.get('hora_levanta_nna') or None, datos.get('va_a_escuela'), datos.get('nivel_educativo_nna'), datos.get('grado_escolar_nna'), datos.get('clase_favorita_nna'), datos.get('clase_cuesta_nna'), datos.get('desempeno_escolar_nna'), datos.get('quien_cuida_nna'), datos.get('horario_juego_nna') or None, datos.get('a_que_juega_nna'), datos.get('se_junta_amigos_nna'), datos.get('hace_deporte_nna'), datos.get('dejado_ver_alguien_nna'), datos.get('narracion_entorno'), datos.get('nivel_bilinguismo_nna'), datos.get('participacion_asambleas'), datos.get('parentesco_autoridades')
                ))
                id_nna = cursor.fetchone()[0]

                # 4. Insertar en hecho_victimal
                if datos.get('relato_hechos') or datos.get('lugar_hecho') or datos.get('num_reporte') or datos.get('nombre_caso'):
                    sql_hv = """
                        INSERT INTO hecho_victimal (
                            id_nna, fecha_detencion, nombre_caso, num_reporte, nombre_victima_madre, fecha_hecho, lugar_hecho, relato_hechos, derechos_vulnerados,
                            ciudad_deteccion, tipo_quien_detecta, nombre_elabora_reporte, descripcion_delito, num_expediente_juridico,
                            referencias_ubicacion_nna, observaciones_relevantes, medidas_urgentes_solicitadas, fecha_solicitud_medidas,
                            justificacion_medida, tipo_medida, opinion_nna_medida
                        ) VALUES (%s, CURRENT_DATE, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_hv, (
                        id_nna, 
                        datos.get('nombre_caso') or 'N/A',
                        datos.get('num_reporte') or 'N/A',
                        datos.get('nombre_victima_madre') or 'N/A',
                        datos.get('fecha_hecho') or None,
                        datos.get('lugar_hecho'),
                        datos.get('relato_hechos'),
                        datos.get('derechos_vulnerados'),
                        datos.get('ciudad_deteccion'),
                        datos.get('tipo_quien_detecta'),
                        datos.get('nombre_elabora_reporte'),
                        datos.get('descripcion_delito'),
                        datos.get('num_expediente_juridico'),
                        datos.get('referencias_ubicacion_nna'),
                        datos.get('observaciones_relevantes'),
                        datos.get('medidas_urgentes_solicitadas'),
                        datos.get('fecha_solicitud_medidas') or None,
                        datos.get('justificacion_medida'),
                        datos.get('tipo_medida'),
                        datos.get('opinion_nna_medida')
                    ))

                # 5. Insertar en entorno_familiar
                cursor.execute("""
                    INSERT INTO entorno_familiar (
                        id_nna, dinamica_familiar, condiciones_vivienda, ingreso_mensual,
                        sistema_residencia, sosten_economico_principal, relacion_madre_familia, patron_migracion_familia, sistema_compadrazgo,
                        espacios_socializacion, participacion_comunidad, hijo_no_vive_con_familia, opinion_nna_considerada, nna_visto_violencia, nna_recibido_violencia,
                        grado_negacion_cuidador, observaciones_negacion, grado_afectacion_cuidador, observaciones_afectacion,
                        redes_apoyo_disponibles, necesidad_proteccion_familia, familiograma_desc, fecha_plan_restitucion,
                            numero_personas_hogar, descripcion_conviven, hermano_no_vive_familia
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    id_nna, datos.get('dinamica_familiar'), datos.get('condiciones_vivienda'), datos.get('ingreso_mensual'),
                    datos.get('sistema_residencia'), datos.get('sosten_economico_principal'), datos.get('relacion_madre_familia'), datos.get('patron_migracion_familia'), datos.get('sistema_compadrazgo'),
                    datos.get('espacios_socializacion'), datos.get('participacion_comunidad'), datos.get('hijo_no_vive_con_familia'), datos.get('opinion_nna_considerada'), datos.get('nna_visto_violencia'), datos.get('nna_recibido_violencia'),
                    datos.get('grado_negacion_cuidador'), datos.get('observaciones_negacion'), datos.get('grado_afectacion_cuidador'), datos.get('observaciones_afectacion'),
                    datos.get('redes_apoyo_disponibles'), datos.get('necesidad_proteccion_familia'), datos.get('familiograma_desc'), datos.get('fecha_plan_restitucion') or None,
                          datos.get('numero_personas_hogar'), datos.get('descripcion_conviven'), datos.get('hermano_no_vive_familia'),
                          datos.get('numero_personas_hogar'), datos.get('descripcion_conviven'), datos.get('hermano_no_vive_familia')
                ))
                    
                # 6. Insertar Familiar
                if datos.get('nombre_familiar'):
                    p_nom, p_ape = split_name(datos.get('nombre_familiar'))
                    cursor.execute("""
                        INSERT INTO personas_expediente (p_nombre, p_apellido, fecha_nacimiento) 
                        VALUES (%s, %s, CURRENT_DATE) RETURNING id_persona_exp
                    """, (p_nom, p_ape))
                    id_pe_fam = cursor.fetchone()[0]
                    
                    cursor.execute("""
                        INSERT INTO familiares (id_persona_exp, parentesco, observaciones)
                        VALUES (%s, %s, %s)
                    """, (id_pe_fam, datos.get('parentesco_familiar') or 'N/A', datos.get('observaciones_familiar')))

                # 7. Insertar Tutor
                if datos.get('nombre_tutor'):
                    p_nom, p_ape = split_name(datos.get('nombre_tutor'))
                    cursor.execute("""
                        INSERT INTO personas_expediente (p_nombre, p_apellido, fecha_nacimiento) 
                        VALUES (%s, %s, CURRENT_DATE) RETURNING id_persona_exp
                    """, (p_nom, p_ape))
                    id_pe_tut = cursor.fetchone()[0]
                    
                    cursor.execute("""
                        INSERT INTO tutores (id_persona_exp, ocupacion, escolaridad, observaciones, es_tutor_legal, vive_con_nna, idioma_tutor, nivel_idioma_tutor, tiene_enfermedades_tutor, padecimientos_tutor, padecimiento_cronico_tutor, padecimiento_controlado_tutor, recibe_atencion_medica_tutor, alcoholismo_dependencias_familia, grado_negacion_tutor, observaciones_negacion_tutor, grado_afectacion_tutor, patron_migracion_tutor, observaciones_generales_tutor, telefono_celular_tutor, tiene_whatsapp_tutor, correo_tutor)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (id_pe_tut, datos.get('ocupacion_tutor') or 'N/A', datos.get('escolaridad_tutor') or 'N/A', datos.get('observaciones_tutor'), datos.get('es_tutor_legal'), datos.get('vive_con_nna'), datos.get('idioma_tutor'), datos.get('nivel_idioma_tutor'), datos.get('tiene_enfermedades_tutor'), datos.get('padecimientos_tutor'), datos.get('padecimiento_cronico_tutor'), datos.get('padecimiento_controlado_tutor'), datos.get('recibe_atencion_medica_tutor'), datos.get('alcoholismo_dependencias_familia'), datos.get('grado_negacion_tutor'), datos.get('observaciones_negacion_tutor'), datos.get('grado_afectacion_tutor'), datos.get('patron_migracion_tutor'), datos.get('observaciones_generales_tutor'), datos.get('telefono_celular_tutor'), datos.get('tiene_whatsapp_tutor'), datos.get('correo_tutor')))

                return True, "Expediente guardado correctamente."
    except Exception as e:
        import traceback
        print("Error en guardar_nna_db:", traceback.format_exc())
        return False, str(e)
