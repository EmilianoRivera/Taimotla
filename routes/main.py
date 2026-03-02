from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from models.auth import verify_director

bp_main = Blueprint("main", __name__)

@bp_main.route("/")
def index() :
    return render_template("main/index.html")

@bp_main.route("/conocenos")
def conocenos():
    return render_template("main/conocenos.html")

@bp_main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("correo")
        password = request.form.get("contrasena")

        response = verify_director(email)
        print(response)
        if response and check_password_hash(response[1], password):
            session['user_id'] = response[0] # EL USER_ID no es un numero es el CURP!
            session['rol']='director'
            session['nombre']=response[2]

            return redirect(url_for("director.dashboard"))
    return render_template("main/login.html")