from flask import render_template, request, redirect, url_for, flash, session
from models import db, Task
from flask import Blueprint

todo_bp = Blueprint('todo', __name__, url_prefix='/todo')

def login_required(func):
    """Decorator to require login for certain routes."""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@todo_bp.route('/')
@login_required
def todo_list():
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()  # Filtrar tareas del usuario
    return render_template('todo_list.html', tasks=tasks)

@todo_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title', '').strip()
    if not title:
        flash('El título es obligatorio.', 'error')
        return redirect(url_for('todo.todo_list'))
    
    user_id = session['user_id']
    new_task = Task(title=title, user_id=user_id)  # Asignar tarea al usuario
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('todo.todo_list'))

@todo_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:  # Verificar que la tarea pertenece al usuario
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('todo.todo_list'))
    
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todo.todo_list'))
