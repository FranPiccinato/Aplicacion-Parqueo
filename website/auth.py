from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Usuario, Parqueo, Vehiculo
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo') # Obtiene los valores del form
        contra = request.form.get('contrasena')

        usuario = Usuario.query.filter_by(correo=correo).first() #Obtiene el primer usuario donde el correo sea igual al correo ingresado 
        if usuario: # Si existe
            if usuario.contra == contra or check_password_hash(usuario.contra, contra):
                if usuario.contra == 'Ulacit123': # Si la contraseña es Ulacit123 redirige a la pantalla de cambio de contraseña
                    return redirect(url_for('auth.cambioLogin'))
                else:
                    login_user(usuario, remember=True) # Recuerda el usuario que se encuentra ingresado
                    if usuario.rol == 'Estudiante' or usuario.rol == 'Administrativo':
                        flash('En progreso', category='success')
                    elif usuario.rol == 'Administrador': # Si ingresa un Admin redirige a la pantalla del admin
                        return redirect(url_for('auth.registrarUsuarios'))
                    elif usuario.rol == 'Oficial': 
                        flash('En progreso', category='success')
            else:
                flash('Contraseña incorrecta',  category='error')  
        else:
            flash('Usuario incorrecta',  category='error')  
            
    return render_template("/login.html") # Carga login.html

@auth.route('/registrar-usuarios', methods=['GET', 'POST'])
def registrarUsuarios():
    if request.method == 'POST': 
        nombre = request.form.get('nombreUsuario') # Obtiene los valores del form
        id = request.form.get('idUsuario')
        correo = request.form.get('correoUsuario')
        nCarne = request.form.get('noUsuario')
        fecha = request.form.get('fechaUsuario')
        rol = request.form.get('rol')
     

        if len(nombre) < 2:
            flash('El nombre debe de contener más de 2 carácteres.',  category='error')
        elif len(correo) < 4:
            flash('El correo debe de contener más de 4 carácteres.',  category='error')
            pass
        else:
            nuevoUsuario = Usuario(id=id, nombre=nombre, correo=correo, nCarne=nCarne, fecha= fecha, rol=rol, contra = 'Ulacit123') # Crea un nuevo usuario y pone la contraseña por default
            db.session.add(nuevoUsuario) # Se agrega a la base de datos
            db.session.commit()  # Hace un commit a la base de datos para guardar los datos
            flash('Cuenta creada con éxito.',  category='success')
        
    return render_template("admin_usuarios.html") # Carga admin_usuarios.html

@auth.route('/registrar-parqueos', methods=['GET', 'POST'])
def registrarParqueos():
    if request.method == 'POST':
        nombre = request.form.get('nombreParqueo') # Obtiene los valores del form
        capacidadES = request.form.get('capacidadES')
        capacidadMotos = request.form.get('capacidadMoto')
        capacidadLey = request.form.get('capacidadLey')
     

        if len(nombre) < 2:
            flash('El nombre debe de contener más de 2 carácteres.',  category='error')
        else:
            nuevoParqueo = Parqueo(nombre=nombre, capacidadES=capacidadES , capacidadMotos=capacidadMotos, capacidadLey= capacidadLey) # Crea un nuevo parqueo
            db.session.add(nuevoParqueo)  # Se agrega a la base de datos
            db.session.commit()  # Hace un commit a la base de datos para guardar los datos
            flash('Parqueo creado con éxito.',  category='success')
    return render_template("admin_parqueos.html") # Carga admin_parqueos.html

@auth.route('/registrar-vehiculos', methods=['GET', 'POST'])
def registrarVehiculos():

    if request.method == 'POST':
        marca = request.form.get('marcaVehiculo') # Obtiene los valores del form
        tipo = request.form.get('tipoVehiculo')
        color = request.form.get('colorVehiculo')
        dueno = request.form.get('duenoVehiculo')
        placa = request.form.get('noPlaca')
        espacio = request.form.get('espacioLey')

        ley = False
        if espacio == 'on': 
            ley = True
        else:
            ley = False

        if len(marca) < 2:
            flash('La marca debe de contener más de 2 carácteres.',  category='error')
        else:
            nuevoVehiculo = Vehiculo(marca=marca, tipo=tipo , color=color, dueno= dueno, placa = placa, espacio=ley, id_usuario = dueno) # Crea un nuevo vehículo
            db.session.add(nuevoVehiculo) # Se agrega a la base de datos
            db.session.commit() # Hace un commit a la base de datos para guardar los datos
            flash('Vehículo creado con éxito.',  category='success')
      

    return render_template("admin_vehiculos.html",  usuario= Usuario.query.all()) # Carga admin_vehículos.html y pasa la variable usuario para utilizarla en el archivo .html

@auth.route('/cambio', methods=['GET', 'POST'])
def cambioLogin():
    if request.method == 'POST':
        nuevaContra = request.form.get('cambioContrasena') # Obtiene los valores del form
        contra = request.form.get('confirmarContrasena')
        id = current_user.id
        if nuevaContra == contra: # Verifica que las contraseñas sean iguales
            usuario = Usuario.query.filter_by(id=id).first() # Obtiene el usuario 
            usuario.contra = generate_password_hash(nuevaContra, method='pbkdf2:sha256') # Se hace un UPDATE de la contrasena y se utiliza un método para encriptar la contrasena
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