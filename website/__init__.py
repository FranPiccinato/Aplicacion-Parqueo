from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
BD_NAME = "BD Parqueo" 
user = "grupo6"
password = "proyectoParqueo"
server = "db-1.ct5z7jqqy8k7.us-east-1.rds.amazonaws.com"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Grupo6'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://fran:dbprueba@localhost:5432/prueba' 
    
    db.init_app(app) # Inicialización de la base de datos

    from .views import views # Registrar los Blueprints 
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Usuario

    with app.app_context(): 
      db.create_all() # Crea las tablas de la base de datos sino existen 

    login_manager = LoginManager() # Gestor de inicio de sesión
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Inicie sesión primero'
    login_manager.init_app(app)

    @login_manager.user_loader # Carga el usuario
    def load_user(id):
        return Usuario.query.get(int(id))

    return app
