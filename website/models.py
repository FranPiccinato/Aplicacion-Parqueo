from . import db
import re
from sqlalchemy import func
from flask import flash, redirect, url_for, render_template
from flask_login import UserMixin, login_user # Métodos para manejar la gestión de sesiones y autenticación 

class Usuario(db.Model, UserMixin): # Modelo SQLAlchemy para le estructura de la tabla

    id = db.Column(db.Integer, primary_key=True)
    
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True)
    fecha = db.Column(db.Date, nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    contra = db.Column(db.String(150), nullable=False)
    nCarne = db.Column(db.Integer, nullable=True)
    vehiculo = db.relationship('Vehiculo')
      
    def loginUsuario(correo, contra):
        usuario = Usuario.query.filter_by(correo=correo.lower()).first() #Obtiene el primer usuario donde el correo sea igual al correo ingresado 
        if usuario: # Si existe
            if usuario.contra == contra:
                if usuario.contra == 'Ulacit123': # Si la contraseña es Ulacit123 redirige a la pantalla de cambio de contraseña
                    login_user(usuario, remember=True)
                    return redirect(url_for('auth.cambioLogin'))
                else:
                    login_user(usuario, remember=True) # Recuerda el usuario que se encuentra ingresado
                    if usuario.rol == 'Estudiante' or usuario.rol == 'Personal Administrativo':
                        flash('En progreso', category='success')
                    elif usuario.rol == 'Administrador': # Si ingresa un Admin redirige a la pantalla del admin
                        return redirect(url_for('auth.registrarUsuarios'))
                    elif usuario.rol == 'Guarda': 
                        return redirect(url_for('auth.inicioParqueo'))
            else:
                flash('Contraseña incorrecta',  category='error')  
        else:
            flash('Usuario incorrecto',  category='error') 
        return render_template("login.html", correo=correo)


class Administrador(Usuario):

    def registrarUsuario(nombre, id, correo, nCarne, fecha, rol, self):
        existeCarne = None
        existeCorreo = Usuario.query.filter_by(correo=correo).first() 
        existeId = Usuario.query.filter_by(id=id).first()
        
        nAccion = 0
        if nCarne != '':
            existeCarne = Usuario.query.filter_by(nCarne=nCarne).first()
            
        if len(nombre) < 1:
            flash('El nombre debe de contener más de 1 carácter.',  category='error')
        elif len(correo) < 4:
            flash('El correo debe de contener más de 4 caracteres.',  category='error')
        elif existeCorreo:
            flash(f'El correo {correo} ya está registrado',  category='error')
        elif existeCarne and rol == "Estudiante":
            flash(f'El número de carné {nCarne} ya está registrado',  category='error')
        elif len(nCarne) > 0 and rol != "Estudiante":
            flash('El número de carné es solo para el rol Estudiante',  category='error')
        elif existeId:
            flash(f'La identificación {id} ya está registrada',  category='error')
        elif len(id) < 1:
            flash('La cédula no puede quedar vacía',  category='error')
        elif nCarne == '' and rol == "Estudiante":
            flash('El número de carné no puede quedar vacío',  category='error')
        elif nCarne == '' and rol != "Estudiante":
            nCarne = None
            nAccion = 1
        else:
            nAccion = 1
        if nAccion == 1:
            nuevoUsuario = self(id=id, nombre=nombre, correo=correo.lower(), nCarne=nCarne, fecha= fecha, rol=rol, contra = 'Ulacit123') # Crea un nuevo usuario y pone la contraseña por default
            db.session.add(nuevoUsuario) # Se agrega a la base de datos
            db.session.commit()  # Hace un commit a la base de datos para guardar los datos
            flash('Cuenta creada con éxito.',  category='success')
            return redirect(url_for('auth.registrarUsuarios'))

        return render_template("admin_usuarios.html", id=id, nombre=nombre, correo=correo, nCarne=nCarne, fecha=fecha, rol=rol )

    def registrarParqueo(nombre, capacidadES, capacidadMotos, capacidadLey):
        existeParqueo= Parqueo.query.filter_by(nombre=nombre).first() 

        if len(nombre) < 2:
            flash('El nombre debe de contener más de 2 caracteres.',  category='error')
        elif existeParqueo:
            flash(f'El parqueo {nombre} ya está registrado',  category='error')
        else:
            nuevoParqueo = Parqueo(nombre=nombre, capacidadRegulares=capacidadES , capacidadMotos=capacidadMotos, capacidadLey= capacidadLey) # Crea un nuevo parqueo
            db.session.add(nuevoParqueo)  # Se agrega a la base de datos
            db.session.commit()  # Hace un commit a la base de datos para guardar los datos
            flash('Parqueo creado con éxito.',  category='success')
            return redirect(url_for('auth.registrarParqueos'))

        return render_template("admin_parqueos.html", nombre=nombre, capacidadES=capacidadES , capacidadMotos=capacidadMotos, capacidadLey= capacidadLey)

    def registrarVehiculo(marca, tipo, color, dueno, placa, espacio):

        cont = 0
        cantidad = Vehiculo.query.filter_by(id_usuario=dueno)
        existePlaca= Vehiculo.query.filter_by(placa=placa).first() 

        for c in cantidad:
            cont += 1
        
        ley = False
        if espacio == 'on': 
            ley = True
        else:
            ley = False

        if len(marca) < 2:
            flash('La marca debe de contener más de 2 caracteres.',  category='error')
        elif len(color) < 2:
            flash('El color debe de contener más de 2 caracteres.',  category='error')
        elif len(placa) < 1:
            flash('La placa debe de contener más de 1 carácter.',  category='error')    
        elif len(placa) > 10:
            flash('La placa puede contener máximo 10 caracteres.',  category='error')
        elif not re.search(r'^(?=[^A-Z]*[A-Z])(?=[^0-9]*[0-9])', placa):
            flash('La placa solo puede contener números y letras',  category='error')      
        elif cont == 2:
             flash('El dueño ya tiene 2 carros registrados.',  category='error')   
        elif existePlaca:
             flash(f'La placa {placa} ya se encuentra registrada.',  category='error')  
        else:
            nuevoVehiculo = Vehiculo(marca=marca, tipo=tipo , color=color, placa = placa, espacio=ley, id_usuario = dueno) # Crea un nuevo vehículo
            db.session.add(nuevoVehiculo) # Se agrega a la base de datos
            db.session.commit() # Hace un commit a la base de datos para guardar los datos
            flash('Vehículo creado con éxito.',  category='success')
    
            return redirect(url_for('auth.registrarVehiculos'))
        return render_template("admin_vehiculos.html", marca=marca, tipo=tipo , color=color, dueno=dueno, placa = placa, espacio=ley, usuario= Usuario.query.all())
    


class Estudiante(Usuario):

    def verEstatus():
        print("En progreso")

class PersonalAdmin(Usuario):
    def verEstatus():
        print("En progreso")
    

class Guarda(Usuario):
    def reportes():
        print("En progreso")


class Parqueo(db.Model): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    capacidadRegulares = db.Column(db.Integer, nullable=False)
    capacidadMotos = db.Column(db.Integer, nullable=False)
    capacidadLey = db.Column(db.Integer, nullable=False)



class Vehiculo(db.Model): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(100), nullable=False)
    espacio = db.Column(db.Boolean, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

