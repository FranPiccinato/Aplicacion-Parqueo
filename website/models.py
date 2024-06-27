from . import db
from flask import flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import UserMixin, login_user # Métodos para manejar la gestión de sesiones y autenticación 

class Usuario(db.Model, UserMixin): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(150), unique=True)
    nCarne = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    rol = db.Column(db.String(20))
    contra = db.Column(db.String(150))
    vehiculo = db.relationship('Vehiculo')

    def loginUsuario(correo, contra):
        usuario = Usuario.query.filter_by(correo=correo).first() #Obtiene el primer usuario donde el correo sea igual al correo ingresado 
        if usuario: # Si existe
            if usuario.contra == contra or check_password_hash(usuario.contra, contra):
                if usuario.contra == 'Ulacit123': # Si la contraseña es Ulacit123 redirige a la pantalla de cambio de contraseña
                    login_user(usuario, remember=True)
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
            flash('Correo incorrecto',  category='error')  
        return redirect(url_for('auth.login'))
    
    def registrarUsuario(nombre, id, correo, nCarne, fecha, rol):
        
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
        return redirect(url_for('auth.registrarUsuarios'))



class Parqueo(db.Model): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True)
    capacidadES = db.Column(db.Integer)
    capacidadMotos = db.Column(db.Integer)
    capacidadLey = db.Column(db.Integer)

    def registrarParqueo(nombre, capacidadES, capacidadMotos, capacidadLey):
        if len(nombre) < 2:
            flash('El nombre debe de contener más de 2 carácteres.',  category='error')
        else:
            nuevoParqueo = Parqueo(nombre=nombre, capacidadES=capacidadES , capacidadMotos=capacidadMotos, capacidadLey= capacidadLey) # Crea un nuevo parqueo
            db.session.add(nuevoParqueo)  # Se agrega a la base de datos
            db.session.commit()  # Hace un commit a la base de datos para guardar los datos
            flash('Parqueo creado con éxito.',  category='success')
    
        return redirect(url_for('auth.registrarParqueos'))



class Vehiculo(db.Model): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    color = db.Column(db.String(100))
    dueno = db.Column(db.String(150))
    placa = db.Column(db.String(100))
    espacio = db.Column(db.Boolean)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def registrarVehiculo(marca, tipo, color, dueno, placa, espacio):
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
        
        return redirect(url_for('auth.registrarVehiculos'))
