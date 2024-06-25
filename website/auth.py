from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/registrar-usuarios')
def registrarUsuarios():
    return render_template("admin_usuarios.html")

@auth.route('/registrar-parqueos')
def registrarParqueos():
    return render_template("admin_parqueos.html")

@auth.route('/registrar-vehiculos')
def registrarVehiculos():
    return render_template("admin_vehiculos.html")

@auth.route('/cambio')
def cambioLogin():
    return render_template("cambioContra.html")