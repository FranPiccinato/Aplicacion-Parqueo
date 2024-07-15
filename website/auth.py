from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from flask_login import login_required, logout_user, current_user
from .models import Usuario, Administrador, Parqueo
from . import db

auth = Blueprint('auth', __name__)

# Inicio de sesión y admin

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo') # Obtiene los valores del form
        contra = request.form.get('contrasena')
        return Administrador.loginUsuario(correo, contra)

            
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
                return Administrador.registrarUsuario(nombre, id, correo, nCarne, fecha, rol, Usuario)
            
            case 'Personal Administrativo':
                return Administrador.registrarUsuario(nombre, id, correo, nCarne, fecha, rol, Usuario)
            
            case 'Guarda':
                return Administrador.registrarUsuario(nombre, id, correo, nCarne, fecha, rol, Usuario)

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
        if len(nuevaContra) < 5:
            flash('La contraseña debe de ser mayor a 5 caracteres', category='error')
        elif nuevaContra == 'Ulacit123':
            flash('Elija otra contraseña', category='error')
        elif not re.search(r'^(?=[^A-Z]*[A-Z])(?=[^0-9]*[0-9])', nuevaContra):
            flash('La contraseña debe contener números y mayúsculas',  category='error')   
        else:
            if nuevaContra == contra: # Verifica que las contraseñas sean iguales
                usuario = Usuario.query.filter_by(id=id).first() # Obtiene el usuario 
                usuario.contra = nuevaContra # Se hace un UPDATE de la contrasena 
                db.session.commit() # Hace un commit a la base de datos para guardar el cambio
                return redirect(url_for('auth.login')) # Redirige a la pantalla de login 
            else:
                flash('Las contraseñas no son iguales', category='error')
        
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
    

# Guardas

@auth.route('/vigilar-parqueo')
@login_required
def inicioParqueo():
    esGuarda()
    return render_template('guarda_inicio.html', parqueo = Parqueo.query.all())

@auth.route('/ingreso-al-parqueo/<nombre>')
@login_required
def ingresoParqueo(nombre):
    esGuarda()
    return render_template('guarda_ingresos.html', id = nombre)


@auth.route('/egreso-parqueo/<nombre>')
@login_required
def egresoParqueo(nombre):
    esGuarda()
    return render_template('guarda_egresos.html', id = nombre)

@auth.route('/reporte-ocupacion/<nombre>')
@login_required
def reporteOcupacion(nombre):
    esGuarda()
    return render_template('guarda_reportes.html', id = nombre)

def esGuarda():
    if current_user.rol != 'Guarda':
        flash('Acceso denegado', category='error')
        return redirect(url_for('auth.logout'))