"""
Módulo de modelos de la aplicación Flask.
Este archivo define las tablas de la base de datos y sus relaciones.
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # Para hashear y verificar contraseñas

# Inicializar la extensión SQLAlchemy para manejar la base de datos
db = SQLAlchemy()

class Task(db.Model):
    """
    Modelo de la tabla 'Task' (Tareas).
    Representa una tarea en la aplicación.
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único de la tarea
    title = db.Column(db.String(100), nullable=False)  # Título de la tarea (no puede ser nulo)
    completed = db.Column(db.Boolean, default=False)  # Estado de la tarea (completada o no, por defecto False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clave foránea que relaciona la tarea con un usuario

    # Relación bidireccional con el modelo User
    user = db.relationship('User', backref='tasks')  # Permite acceder a las tareas desde un usuario y viceversa

class User(db.Model):
    """
    Modelo de la tabla 'User' (Usuarios).
    Representa un usuario en la aplicación.
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único del usuario
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario (único y no nulo)
    password_hash = db.Column(db.String(128), nullable=False)  # Hash de la contraseña (no puede ser nulo)

    def set_password(self, password):
        """
        Hashea la contraseña y la guarda en el campo password_hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return check_password_hash(self.password_hash, password)