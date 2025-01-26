"""
Este archivo es el punto de entrada de la aplicación Flask.
Se encarga de configurar la aplicación, registrar los Blueprints
y definir rutas básicas.
"""

from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from todo import todo_bp  # Blueprint para las rutas de la lista de tareas
from auth import auth_bp  # Blueprint para las rutas de autenticación
from dotenv import load_dotenv  # Para cargar variables de entorno desde un archivo .env
import os

# Inicializar la extensión de migraciones para manejar cambios en la base de datos
migrate = Migrate()

def create_app():
    """
    Función de fábrica para crear y configurar la aplicación Flask.
    Esta función es el punto de entrada principal para la configuración de la app.
    """
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Crear la instancia de la aplicación Flask
    app = Flask(__name__)

    # Configurar la aplicación con variables de entorno
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev_esit'),  # Clave secreta para sesiones (valor por defecto si no está en .env)
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///todo_list.db'),  # URI de la base de datos (SQLite por defecto)
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Desactivar seguimiento de modificaciones para mejorar el rendimiento
        SESSION_TYPE='filesystem',  # Almacenar sesiones en el sistema de archivos
        SESSION_FILE_DIR='./flask_session'  # Carpeta para almacenar las sesiones
    )

    # Crear la carpeta flask_session si no existe
    if not os.path.exists(app.config['SESSION_FILE_DIR']):
        os.makedirs(app.config['SESSION_FILE_DIR'])

    # Importar y configurar la base de datos
    from models import db
    db.init_app(app)  # Inicializar la base de datos con la aplicación Flask
    migrate.init_app(app, db)  # Configurar las migraciones con la aplicación y la base de datos
    Session(app)  # Inicializar la extensión de sesiones

    # Registrar los Blueprints para las rutas de la aplicación
    app.register_blueprint(todo_bp)  # Blueprint para las tareas
    app.register_blueprint(auth_bp)  # Blueprint para la autenticación

    # Ruta principal de la aplicación
    @app.route('/')
    def index():
        """
        Ruta principal que renderiza la página de inicio (index.html).
        """
        return render_template('index.html')
    
    # Ruta para verificar si el usuario está autenticado
    @app.route('/is_authenticated')
    def is_authenticated():
        """
        Ruta que devuelve un JSON indicando si el usuario está autenticado.
        """
        return {'is_authenticated': 'user_id' in session}

    # Devolver la aplicación configurada
    return app