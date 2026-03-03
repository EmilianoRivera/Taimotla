from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from models.auth import verify_director, verify_coordinador

bp_main = Blueprint("main", __name__)


@bp_main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("correo")
        password = request.form.get("contrasena")

        response_director = verify_director(email)
        if response_director and check_password_hash(response_director[1], password):
            session['user_id'] = response_director[0] # EL USER_ID no es un numero es el CURP!
            session['rol']='director'
            session['nombre']=response_director[2]
            return redirect(url_for("director.dashboard"))

        response_coordinador = verify_coordinador(email)
        print(response_coordinador)
        if response_coordinador and check_password_hash(response_coordinador[1], password):
            session['user_id'] = response_coordinador[0] # EL USER_ID no es un numero es el CURP!
            session['rol']='coordinador'
            session['nombre']=response_coordinador[2]
            return redirect(url_for("coordinador.dashboard"))
    return render_template("main/login.html")