from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('El usuario ya existe.', 'error')
                return redirect(url_for('auth.register'))

            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado con éxito.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Error al registrar el usuario.', 'error')
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
        flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('auth.login'))
