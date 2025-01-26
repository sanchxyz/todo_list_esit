"""
Módulo de autenticación de la aplicación Flask.
Este archivo define las rutas y lógica para el registro, inicio de sesión y cierre de sesión de usuarios.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User  # Importar la base de datos y el modelo de usuario
from sqlalchemy.exc import IntegrityError  # Para manejar errores de integridad en la base de datos

# Crear un Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Ruta para el registro de usuarios.
    - GET: Muestra el formulario de registro.
    - POST: Procesa el formulario de registro y crea un nuevo usuario.
    """
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            # Verificar si el usuario ya existe
            if User.query.filter_by(username=username).first():
                return jsonify({'error': 'El usuario ya existe.'}), 400  # Código 400: Solicitud incorrecta

            # Crear nuevo usuario
            new_user = User(username=username)
            new_user.set_password(password)  # Hashear la contraseña antes de guardarla
            db.session.add(new_user)
            db.session.commit()

            # Enviar mensaje de éxito
            return jsonify({'success': 'Se registró exitosamente.'}), 200  # Código 200: Éxito

        except IntegrityError:
            # En caso de error en la base de datos, hacer rollback y devolver un error
            db.session.rollback()
            return jsonify({'error': 'Error al registrar el usuario.'}), 500  # Código 500: Error del servidor

    # Renderizar el formulario de registro si el método es GET
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para el inicio de sesión de usuarios.
    - GET: Muestra el formulario de inicio de sesión.
    - POST: Procesa el formulario de inicio de sesión y autentica al usuario.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # Verificar si el usuario existe y la contraseña es correcta
        if user and user.check_password(password):
            session['user_id'] = user.id  # Guardar el ID del usuario en la sesión
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('todo.todo_list'))  # Redirigir a la lista de tareas
        else:
            # Si el usuario no existe o la contraseña es incorrecta
            return jsonify({'error': 'Usuario no ha sido encontrado'}), 401  # Código 401: No autorizado

    # Renderizar el formulario de inicio de sesión si el método es GET
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    Ruta para el cierre de sesión de usuarios.
    Elimina el ID del usuario de la sesión y redirige al formulario de inicio de sesión.
    """
    session.pop('user_id', None)  # Eliminar el user_id de la sesión
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('auth.login'))  # Redirigir al formulario de inicio de sesión