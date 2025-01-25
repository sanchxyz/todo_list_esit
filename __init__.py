from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from todo import todo_bp
from auth import auth_bp
from dotenv import load_dotenv
import os

migrate = Migrate()

def create_app():
    # Cargar variables de entorno desde .env
    load_dotenv()

    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev_esit'),  # Usar valor por defecto si no está en .env
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///todo_list.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE='filesystem',
        SESSION_FILE_DIR='./flask_session'
    )

    # Crear la carpeta flask_session si no existe
    if not os.path.exists(app.config['SESSION_FILE_DIR']):
        os.makedirs(app.config['SESSION_FILE_DIR'])

    from models import db
    db.init_app(app)  
    migrate.init_app(app, db) 
    Session(app)

    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/is_authenticated')
    def is_authenticated():
        return {'is_authenticated': 'user_id' in session}

    return app