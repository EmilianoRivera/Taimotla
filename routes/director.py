from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.director import user_register, consult_lawyers, consult_social, consult_medic, consult_psico, consult_director, delete_user, desable_user, consult_unable_users, able_user, search_one_user, update_user



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
    return redirect(url_for('main.index'))

@bp_director.route('/cuenta', methods=['GET'])
def cuenta():
    if session.get('rol') != 'director':
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
        return redirect(url_for("main.index"))
    user_found = None
    if request.method == "GET":
        print(curp)
        user_found = search_one_user(curp)
    return render_template('director/editar.html', user= user_found)

@bp_director.route('/actualizar/<curp>', methods=['GET', 'POST'])
def actualizar(curp):
    if session.get('rol') != 'director':
        return redirect(url_for("main.index"))
    form_data = {
        'correo': request.form.get('correo'),
        'telefono': request.form.get('telefono'),
        'calle': request.form.get('calle')
    }

    # 2. Llamar a la función de actualización
    if update_user(curp, form_data):
        flash("¡Datos actualizados correctamente!", "success")
    else:
        flash("Hubo un error al intentar actualizar.", "error")

    # 3. Redirigir al dashboard para ver los cambios
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
        #extraemos especialidad
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
        return redirect(url_for("main.index"))
    
    if request.method == "POST":
        state = desable_user(curp)
        print(state)
    return redirect(url_for("director.dashboard"))


@bp_director.route('/able/<curp>', methods=['POST'])
def able(curp):
    if session.get('rol') != 'director':
        flash("Acceso restringido a Directivos.", "error")
        return redirect(url_for("main.index"))
    
    if request.method == "POST":
        state = able_user(curp)
        print(state)
    return redirect(url_for("director.dashboard"))