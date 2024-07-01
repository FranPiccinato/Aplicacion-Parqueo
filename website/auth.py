from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_login import login_required, logout_user, current_user
from .models import Usuario, Administrador, Estudiante, PersonalAdmin, Guarda
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo') # Obtiene los valores del form
        contra = request.form.get('contrasena')

        return Usuario.loginUsuario(correo, contra)

            
    return render_template("/login.html") # Carga login.html

@auth.route('/registrar-usuarios', methods=['GET', 'POST'])
@login_required
def registrarUsuarios():
    esAdmin()
    if request.method == 'POST': 
        nombre = request.form.get('nombreUsuario') # Obtiene los valores del form
        id = request.form.get('idUsuario')
        correo = request.form.get('correoUsuario')
        nCarne = request.form.get('nCarne')
        fecha = request.form.get('fechaUsuario')
        rol = request.form.get('rol')
        
        match rol:    
            case 'Estudiante':
                return Estudiante.registrarUsuario(nombre, id, correo, nCarne, fecha, rol, Estudiante)
            
            case 'Personal Administrativo':
                return PersonalAdmin.registrarUsuario(nombre, id, correo, nCarne, fecha, rol, PersonalAdmin)
            
            case 'Guarda':
                return Guarda.registrarUsuario(nombre, id, correo, nCarne, fecha, rol, Guarda)

    return render_template("admin_usuarios.html") # Carga admin_usuarios.html

@auth.route('/registrar-parqueos', methods=['GET', 'POST'])
@login_required
def registrarParqueos():
    esAdmin()
    if request.method == 'POST':
        nombre = request.form.get('nombreParqueo') # Obtiene los valores del form
        capacidadES = request.form.get('capacidadES')
        capacidadMotos = request.form.get('capacidadMoto')
        capacidadLey = request.form.get('capacidadLey')

        return Administrador.registrarParqueo(nombre, capacidadES, capacidadMotos, capacidadLey)
    
    return render_template("admin_parqueos.html") # Carga admin_parqueos.html

@auth.route('/registrar-vehiculos', methods=['GET', 'POST'])
@login_required
def registrarVehiculos():
    esAdmin()
    if request.method == 'POST':
        marca = request.form.get('marcaVehiculo') # Obtiene los valores del form
        tipo = request.form.get('tipoVehiculo')
        color = request.form.get('colorVehiculo')
        dueno = request.form.get('duenoVehiculo')
        placa = request.form.get('noPlaca')
        espacio = request.form.get('espacioLey')

        return Administrador.registrarVehiculo(marca, tipo, color, dueno, placa, espacio)
      

    return render_template("admin_vehiculos.html",  usuario= Usuario.query.all()) # Carga admin_vehículos.html y pasa la variable usuario para utilizarla en el archivo .html

@auth.route('/cambio', methods=['GET', 'POST'])
@login_required
def cambioLogin():
    if current_user.contra != 'Ulacit123':
        flash('Acceso denegado', category='error')
        return redirect(url_for('auth.logout'))
    if request.method == 'POST':
        nuevaContra = request.form.get('cambioContrasena') # Obtiene los valores del form
        contra = request.form.get('confirmarContrasena')
        id = current_user.id
        if len(nuevaContra) > 4:
            if nuevaContra == contra: # Verifica que las contraseñas sean iguales
                usuario = Usuario.query.filter_by(id=id).first() # Obtiene el usuario 
                usuario.contra = generate_password_hash(nuevaContra, method='pbkdf2:sha256') # Se hace un UPDATE de la contrasena y se utiliza un método para encriptar la contrasena
                db.session.commit() # Hace un commit a la base de datos para guardar el cambio
                return redirect(url_for('auth.login')) # Redirige a la pantalla de login 
            else:
                flash('Las contraseñas no son iguales', category='error')
        else:
            flash('La contraseña debe de ser mayor a 4 caracteres', category='error')
        
    return render_template("cambioContra.html") # Carga cambioContra.html

@auth.route('/logout') # Cierra sesión del usuario actual
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # Redirige a la pantalla de login 

def esAdmin():
    if current_user.rol != 'Administrador':
        flash('Acceso denegado', category='error')
        return redirect(url_for('auth.logout'))
    
