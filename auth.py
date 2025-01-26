from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            # Verificar si el usuario ya existe
            if User.query.filter_by(username=username).first():
                return jsonify({'error': 'El usuario ya existe.'}), 400  # Código 400: Solicitud incorrecta

            # Crear nuevo usuario
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            # Enviar mensaje de éxito
            return jsonify({'success': 'Se registró exitosamente.'}), 200  # Código 200: Éxito

        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Error al registrar el usuario.'}), 500  # Código 500: Error del servidor

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('todo.todo_list'))  # Redirige a la lista de tareas
        else:
            # Si el usuario no existe o la contraseña es incorrecta
            return jsonify({'error': 'Usuario no ha sido encontrado'}), 401  # Código 401: No autorizado

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Eliminar el user_id de la sesión
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('auth.login'))  # Redirigir al login