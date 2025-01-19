from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from todo import todo_bp


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev_esit',
        SQLALCHEMY_DATABASE_URI='sqlite:///todo_list.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    from models import db
    db.init_app(app)  
    migrate.init_app(app, db) 
    app.register_blueprint(todo_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app