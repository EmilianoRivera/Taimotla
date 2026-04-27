from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models.auth import verify_director, verify_coordinador

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
def index():
    return redirect(url_for("main.login"))


@bp_main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("correo", "").strip()
        password = request.form.get("contrasena", "")

        # ── DIRECTOR ──────────────────────────────────────────────
        # query devuelve: (CURP, p_nombre, contrasena, estado)
        #                   [0]     [1]        [2]       [3]
        response_director = verify_director(email)
        print("DEBUG director →", response_director)

        if response_director:
            curp, nombre, contrasena, estado = response_director

            if estado != 1:
                flash("Tu cuenta de director está deshabilitada.", "error")
                return render_template("main/login.html")

            if check_password_hash(contrasena, password):
                session['user_id'] = curp
                session['rol']     = 'director'
                session['nombre']  = nombre
                return redirect(url_for("director.dashboard"))

        # ── COORDINADOR ───────────────────────────────────────────
        # query devuelve: (CURP, p_nombre, contrasena, estado)
        #                   [0]     [1]        [2]       [3]
        response_coordinador = verify_coordinador(email)
        print("DEBUG coordinador →", response_coordinador)

        if response_coordinador:
            curp, nombre, contrasena, estado = response_coordinador

            if estado != 1:
                flash("Tu cuenta de coordinador está deshabilitada.", "error")
                return render_template("main/login.html")

            if check_password_hash(contrasena, password):
                session['user_id'] = curp
                session['rol']     = 'coordinador'
                session['nombre']  = nombre
                return redirect(url_for("coordinador.dashboard"))

        # ── FALLO ─────────────────────────────────────────────────
        flash("Correo o contraseña incorrectos.", "error")

    return render_template("main/login.html")