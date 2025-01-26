"""
Módulo de gestión de tareas de la aplicación Flask.
Este archivo define las rutas y lógica para listar, agregar y eliminar tareas.
"""

from flask import render_template, request, redirect, url_for, flash, session
from models import db, Task  # Importar la base de datos y el modelo de tarea
from flask import Blueprint
from functools import wraps  # Para crear decoradores

# Crear un Blueprint para las rutas de gestión de tareas
todo_bp = Blueprint('todo', __name__, url_prefix='/todo')

def login_required(func):
    """
    Decorador para asegurar que el usuario esté autenticado antes de acceder a una ruta.
    Si el usuario no está autenticado, se redirige a la página de inicio de sesión.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper

@todo_bp.route('/')
@login_required
def todo_list():
    """
    Ruta para listar las tareas del usuario autenticado.
    - Filtra las tareas por el ID del usuario en la sesión.
    - Renderiza la plantilla 'todo_list.html' con las tareas.
    """
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()  # Filtrar tareas del usuario
    return render_template('todo_list.html', tasks=tasks)

@todo_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    """
    Ruta para agregar una nueva tarea.
    - Verifica que el título de la tarea no esté vacío.
    - Crea una nueva tarea asociada al usuario autenticado.
    - Redirige a la lista de tareas después de agregar la tarea.
    """
    title = request.form.get('title', '').strip()
    if not title:
        flash('El título es obligatorio.', 'error')
        return redirect(url_for('todo.todo_list'))
    
    user_id = session['user_id']
    new_task = Task(title=title, user_id=user_id)  # Crear una nueva tarea asociada al usuario
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('todo.todo_list'))

@todo_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    """
    Ruta para eliminar una tarea.
    - Verifica que la tarea pertenezca al usuario autenticado.
    - Elimina la tarea de la base de datos.
    - Redirige a la lista de tareas después de eliminar la tarea.
    """
    task = Task.query.get_or_404(task_id)  # Obtener la tarea o devolver un error 404 si no existe
    if task.user_id != session['user_id']:  # Verificar que la tarea pertenece al usuario
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('todo.todo_list'))
    
    db.session.delete(task)  # Eliminar la tarea
    db.session.commit()
    return redirect(url_for('todo.todo_list'))