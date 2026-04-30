from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.director import user_register, consult_lawyers, consult_social, consult_medic, consult_psico, consult_director, delete_user, desable_user, consult_unable_users, able_user, search_one_user, update_user
from models.equipo import get_all_coordinators, get_available_staff, get_busy_staff, create_team
import json



bp_director = Blueprint('director', __name__, url_prefix='/director')

@bp_director.route('/dashboard', methods=['GET'])
def dashboard():
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    if request.method=='GET':
        data_lawyers = consult_lawyers()
        data_social =consult_social()
        data_medics = consult_medic()
        data_psico = consult_psico()
        data_users_unable = consult_unable_users()
        print(data_medics)
        print(data_psico)
        print(data_social)
        print(data_lawyers)

    return render_template('director/dashboard.html', nombre=session['nombre'], users_lawyers=data_lawyers, users_social = data_social, users_psico = data_psico, users_medics = data_medics, users_unable = data_users_unable)

@bp_director.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('main.login'))

@bp_director.route('/cuenta', methods=['GET'])
def cuenta():
    if session.get('rol') != 'director' :
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    if request.method == 'GET':
        curp = session.get('user_id')
        data_director = consult_director(str(curp))
        print(data_director)
    return render_template('director/cuenta.html', nombre=session['nombre'], user_director = data_director)

@bp_director.route('/editar/<curp>', methods=['GET', 'POST'])
def editar(curp):
    if session.get('rol') != 'director':
        return redirect(url_for("main.login"))
    user_found = None
    if request.method == "GET":
        user_found = search_one_user(curp)
    return render_template('director/editar.html', user= user_found)

@bp_director.route('/actualizar/<curp>', methods=['GET', 'POST'])
def actualizar(curp):
    if session.get('rol') != 'director':
        return redirect(url_for("main.login"))
    form_data = {
        'rfc': request.form.get('rfc'),
        'p_nombre': request.form.get('p_nombre'),
        's_nombre': request.form.get('s_nombre'),
        'p_apellido': request.form.get('p_apellido'),
        's_apellido': request.form.get('s_apellido'),
        'sexo': request.form.get('sexo'),
        'fecha_nacimiento': request.form.get('fecha_nacimiento'),
        'calle': request.form.get('calle'),
        'num_ext': request.form.get('num_ext'),
        'colonia': request.form.get('colonia'),
        'cp': request.form.get('cp'),
        'municipio': request.form.get('municipio'),
        'estado_rep': request.form.get('estado_rep'),
        'telefono': request.form.get('telefono'),
        'correo': request.form.get('correo')
    }

    if update_user(curp, form_data):
        flash("¡Datos actualizados correctamente!", "success")
    else:
        flash("Hubo un error al intentar actualizar.", "error")

    return redirect(url_for('director.dashboard'))





@bp_director.route('/eliminar/<curp>', methods=["POST"])
def eliminar(curp):
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    if request.method == 'POST':
   
        eliminar = delete_user(curp)
    return redirect(url_for("director.dashboard"))

@bp_director.route('/registrar', methods=['GET','POST'])
def registrar():
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    if request.method=='POST':
        data = {
            'curp': request.form.get("curp").upper(),
            'rfc': request.form.get("rfc").upper(),
            'p_nombre':request.form.get("p_nombre"),
            's_nombre':request.form.get("s_nombre"),
            'p_apellido':request.form.get("p_apellido"),
            's_apellido':request.form.get("s_apellido"),
            'fecha_nacimiento':request.form.get("fecha_nacimiento"),
            'sexo':request.form.get("sexo"),
            'correo':request.form.get("correo"),
            'telefono':request.form.get("telefono"),
            'calle':request.form.get("calle"),
            'num_ext':request.form.get("num_ext"),
            'colonia':request.form.get("colonia"),
            'cp':request.form.get("cp"),
            'municipio':request.form.get("municipio"),
            'estado_rep':request.form.get("estado_rep"),
            'rol':request.form.get("rol"),
            'tipo':request.form.get("tipo"),
            'cedula':request.form.get("cedula"),
            'contrasena':request.form.get("contrasena")
        }
        rol = request.form.get("rol")
        if rol == 'abogado' :
            data['especialidad'] = request.form.get("esp_abogado")
        elif rol == 'medico':
            data['especialidad'] = request.form.get("esp_medico")
        elif rol == 'psicologo':
            data['especialidad'] = request.form.get("enfoque_psicologo")
        user_register(data)
        flash("Usuario registrado con exito", "success")

        return redirect(url_for("director.dashboard"))
    return render_template('director/registrar.html')


@bp_director.route('/desable/<curp>', methods=['POST'])
def desable(curp):
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for("main.login"))
    
    if request.method == "POST":
        state = desable_user(curp)
        print(state)
    return redirect(url_for("director.dashboard"))


@bp_director.route('/able/<curp>', methods=['POST'])
def able(curp):
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for("main.login"))
    
    if request.method == "POST":
        state = able_user(curp)
        print(state)
    return redirect(url_for("director.dashboard"))

@bp_director.route('/crear_equipo', methods=['GET', 'POST'])
def crear_equipo():
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
        
    if request.method == 'POST':
        nombre_equipo = request.form.get('nombre_equipo')
        curp_coordinador = request.form.get('curp_coordinador')
        integrantes = request.form.get('integrantes')
        
        try:
            integrantes_curps = json.loads(integrantes)
        except Exception:
            flash("Error al procesar los integrantes.", "error")
            return redirect(url_for('director.crear_equipo'))
            
        if len(integrantes_curps) < 2 or len(integrantes_curps) > 4:
            flash("El equipo debe tener entre 2 y 4 integrantes.", "error")
            return redirect(url_for('director.crear_equipo'))
            
        success, msg = create_team(nombre_equipo, curp_coordinador, integrantes_curps)
        if success:
            flash(msg, "success")
            return redirect(url_for('director.dashboard'))
        else:
            flash(msg, "error")
            return redirect(url_for('director.crear_equipo'))

    coordinators = get_all_coordinators()
    available_staff = get_available_staff()
    busy_staff = get_busy_staff()
    
    return render_template('director/crear_equipo.html', 
                           coordinators=coordinators, 
                           available_staff=available_staff, 
                           busy_staff=busy_staff)
from models.equipo import get_active_teams, add_member_to_team, remove_member_from_team, update_team_coordinator, delete_team

@bp_director.route('/equipos', methods=['GET'])
def equipos():
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    
    equipos_list = get_active_teams()
    coordinadores = get_all_coordinators()
    disponibles = get_available_staff()
    
    return render_template('director/equipos.html', equipos=equipos_list, coordinadores=coordinadores, disponibles=disponibles)

@bp_director.route('/equipos/<int:id_equipo>/eliminar', methods=['POST'])
def eliminar_equipo(id_equipo):
    if session.get('rol') != 'director': return redirect(url_for('main.login'))
    success, msg = delete_team(id_equipo)
    if success: flash(msg, "success")
    else: flash(msg, "error")
    return redirect(url_for('director.equipos'))

@bp_director.route('/equipos/<int:id_equipo>/coordinador', methods=['POST'])
def actualizar_coordinador(id_equipo):
    if session.get('rol') != 'director': return redirect(url_for('main.login'))
    curp = request.form.get('curp_coordinador')
    success, msg = update_team_coordinator(id_equipo, curp)
    if success: flash(msg, "success")
    else: flash(msg, "error")
    return redirect(url_for('director.equipos'))

@bp_director.route('/equipos/<int:id_equipo>/agregar', methods=['POST'])
def agregar_miembro_equipo(id_equipo):
    if session.get('rol') != 'director': return redirect(url_for('main.login'))
    curp = request.form.get('curp_miembro')
    success, msg = add_member_to_team(id_equipo, curp)
    if success: flash(msg, "success")
    else: flash(msg, "error")
    return redirect(url_for('director.equipos'))

@bp_director.route('/equipos/<int:id_equipo>/remover', methods=['POST'])
def remover_miembro_equipo(id_equipo):
    if session.get('rol') != 'director': return redirect(url_for('main.login'))
    curp = request.form.get('curp_miembro')
    success, msg = remove_member_from_team(id_equipo, curp)
    if success: flash(msg, "success")
    else: flash(msg, "error")
    return redirect(url_for('director.equipos'))

@bp_director.route('/expediente', methods=['GET'])
def expediente():
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    
    from models.database import get_db_cursor
    
    catalogo_sexo = []
    catalogo_etnia = []
    catalogo_nacionalidad = []
    
    try:
        with get_db_cursor() as (cursor, conn):
            cursor.execute("SELECT id_sexo, sexo FROM sexo ORDER BY id_sexo")
            catalogo_sexo = cursor.fetchall()
            
            cursor.execute("SELECT id_etnia, nombre_etnia FROM etnia ORDER BY nombre_etnia")
            catalogo_etnia = cursor.fetchall()
            
            cursor.execute("SELECT id_nacionalidad, nombre_nacionalidad FROM nacionalidad ORDER BY nombre_nacionalidad")
            catalogo_nacionalidad = cursor.fetchall()
    except Exception as e:
        print("Error fetching catalogues:", e)
        
    return render_template('director/expediente.html',
                           sexos=catalogo_sexo,
                           etnias=catalogo_etnia,
                           nacionalidades=catalogo_nacionalidad)

from flask import jsonify, request
from models.nna import buscar_nna_db, obtener_datos_nna_db, guardar_nna_db

@bp_director.route('/api/buscar_nna', methods=['GET'])
def api_buscar_nna():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    resultados = buscar_nna_db(query)
    return jsonify(resultados)

@bp_director.route('/api/obtener_nna/<int:id_nna>', methods=['GET'])
def api_obtener_nna(id_nna):
    datos = obtener_datos_nna_db(id_nna)
    return jsonify(datos)

@bp_director.route('/expediente/guardar', methods=['POST'])
def guardar_expediente():
    if session.get('rol') != 'director':
        return jsonify({"error": "No autorizado"}), 403

    datos = request.form.to_dict()
    exito, mensaje = guardar_nna_db(datos)
    
    if exito:
        flash(mensaje, "success")
    else:
        flash(f"Error al guardar expediente: {mensaje}", "error")
        
    return redirect(url_for('director.expediente'))
