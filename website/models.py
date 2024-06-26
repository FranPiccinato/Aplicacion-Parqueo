from . import db
from flask_login import UserMixin # Métodos para manejar la gestión de sesiones y autenticación 

class Usuario(db.Model, UserMixin): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(150), unique=True)
    nCarne = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    rol = db.Column(db.String(20))
    contra = db.Column(db.String(150))
    vehiculo = db.relationship('Vehiculo')

class Parqueo(db.Model): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True)
    capacidadES = db.Column(db.Integer)
    capacidadMotos = db.Column(db.Integer)
    capacidadLey = db.Column(db.Integer)

class Vehiculo(db.Model): # Modelo SQLAlchemy para le estructura de la tabla
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    color = db.Column(db.String(100))
    dueno = db.Column(db.String(150))
    placa = db.Column(db.String(100))
    espacio = db.Column(db.Boolean)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
