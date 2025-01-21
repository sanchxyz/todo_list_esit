from flask import render_template, request, redirect, url_for, flash
from models import db, Task
from flask import Blueprint

todo_bp = Blueprint('todo', __name__, url_prefix='/todo')

@todo_bp.route('/')
def todo_list():
    tasks = Task.query.all()
    return render_template('todo_list.html', tasks=tasks)

@todo_bp.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Title is required!', 'error')  # Mensaje de error.
        return redirect(url_for('todo.todo_list'))
    
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('todo.todo_list'))

@todo_bp.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Manejo de errores automático.
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todo.todo_list'))