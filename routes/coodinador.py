from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.director import user_register, consult_lawyers, consult_social, consult_medic, consult_psico, delete_user, desable_user, consult_unable_users, able_user, search_one_user, update_user

from models.coordinador import  consult_coordinador


bp_coordinador = Blueprint('coordinador', __name__, url_prefix='/coordinador')

@bp_coordinador.route('/dashboard', methods=['GET'])
def dashboard():
    if session.get('rol') != 'coordinador':
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

    return render_template('coordinador/dashboard.html', nombre=session['nombre'], users_lawyers=data_lawyers, users_social = data_social, users_psico = data_psico, users_medics = data_medics, users_unable = data_users_unable)

@bp_coordinador.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('main.index'))

@bp_coordinador.route('/cuenta', methods=['GET'])
def cuenta():
    if session.get('rol') != 'coordinador':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    if request.method == 'GET':
        curp = session.get('user_id')
        data_coordinador = consult_coordinador(str(curp))
        print(data_coordinador)
    return render_template('coordinador/cuenta.html', nombre=session['nombre'], user_coordinador = data_coordinador)

@bp_coordinador.route('/editar/<curp>', methods=['GET', 'POST'])
def editar(curp):
    if session.get('rol') != 'coordinador':
        return redirect(url_for("main.index"))
    user_found = None
    if request.method == "GET":
        print(curp)
        user_found = search_one_user(curp)
    return render_template('coordinador/editar.html', user= user_found)

@bp_coordinador.route('/actualizar/<curp>', methods=['GET', 'POST'])
def actualizar(curp):
    if session.get('rol') != 'coordinador':
        return redirect(url_for("main.index"))
    form_data = {
        'correo': request.form.get('correo'),
        'telefono': request.form.get('telefono'),
        'calle': request.form.get('calle')
    }

    if update_user(curp, form_data):
        flash("¡Datos actualizados correctamente!", "success")
    else:
        flash("Hubo un error al intentar actualizar.", "error")

    return redirect(url_for('coordinador.dashboard'))


@bp_coordinador.route('/eliminar/<curp>', methods=["POST"])
def eliminar(curp):
    if session.get('rol') != 'coordinador':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for('main.login'))
    if request.method == 'POST':
   
        eliminar = delete_user(curp)
    return redirect(url_for("coordinador.dashboard"))

@bp_coordinador.route('/registrar', methods=['GET','POST'])
def registrar():
    if session.get('rol') != 'coordinador':
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

        return redirect(url_for("coordinador.dashboard"))
    return render_template('coordinador/registrar.html')


@bp_coordinador.route('/desable/<curp>', methods=['POST'])
def desable(curp):
    if session.get('rol') != 'coordinador':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for("main.login"))
    
    if request.method == "POST":
        state = desable_user(curp)
        print(state)
    return redirect(url_for("coordinador.dashboard"))


@bp_coordinador.route('/able/<curp>', methods=['POST'])
def able(curp):
    if session.get('rol') != 'coordinador':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for("main.login"))
    
    if request.method == "POST":
        state = able_user(curp)
        print(state)
    return redirect(url_for("coordinador.dashboard"))