from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Task, TaskCategory
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

# ---------------- DASHBOARD ----------------
@tasks_bp.route('/')
@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()

    # Task statistics
    total_tasks = len(tasks)
    pending_tasks = len([t for t in tasks if t.status == 'pending'])
    in_progress_tasks = len([t for t in tasks if t.status == 'in_progress'])
    completed_tasks = len([t for t in tasks if t.status == 'completed'])

    # Overdue tasks (naive UTC)
    overdue_tasks = [
        t for t in tasks
        if t.due_date and t.due_date < datetime.utcnow() and t.status != 'completed'
    ]

    categories = TaskCategory.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'tasks/dashboard.html',
        tasks=tasks,
        categories=categories,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        now=datetime.utcnow()
    )

# ---------------- ADD TASK ----------------
@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority', 'medium')
    due_date_str = request.form.get('due_date')
    category_id = request.form.get('category_id')

    if not title:
        flash('Task title is required', 'danger')
        return redirect(url_for('tasks.dashboard'))

    if priority not in Task.PRIORITY_CHOICES:
        priority = 'medium'

    due_date = None
    if due_date_str:
        try:
            if 'T' in due_date_str:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
            else:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid due date format', 'danger')
            return redirect(url_for('tasks.dashboard'))

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        user_id=current_user.id
    )

    if category_id:
        category = TaskCategory.query.filter_by(id=category_id, user_id=current_user.id).first()
        if category:
            new_task.category = category

    try:
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while adding the task', 'danger')

    return redirect(url_for('tasks.dashboard'))

# ---------------- EDIT TASK ----------------
@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    categories = TaskCategory.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        due_date_str = request.form.get('due_date')

        task.title = title
        task.description = description
        task.priority = priority if priority in Task.PRIORITY_CHOICES else task.priority

        if due_date_str:
            try:
                if 'T' in due_date_str:
                    task.due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
                else:
                    task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid due date format', 'danger')
                return redirect(url_for('tasks.edit_task', task_id=task_id))
        else:
            task.due_date = None

        try:
            db.session.commit()
            flash('Task updated successfully', 'success')
            return redirect(url_for('tasks.dashboard'))
        except Exception:
            db.session.rollback()
            flash('An error occurred while updating the task', 'danger')

    return render_template(
    'tasks/edit_task.html',
    task=task,
    categories=categories,
    due_date_str=task.due_date.strftime('%Y-%m-%dT%H:%M') if task.due_date else '',
    now=datetime.utcnow()  # pass 'now' for template comparisons
)

# ---------------- DELETE TASK ----------------
@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting the task', 'danger')

    return redirect(url_for('tasks.dashboard'))

# ---------------- TOGGLE TASK STATUS ----------------
@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

    if task.status == 'pending':
        task.status = 'in_progress'
    elif task.status == 'in_progress':
        task.status = 'completed'
        task.completed_at = datetime.utcnow()
    else:
        task.status = 'pending'
        task.completed_at = None

    try:
        db.session.commit()
        flash(f'Task status changed to {task.status}', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while updating the task', 'danger')

    return redirect(url_for('tasks.dashboard'))

# ---------------- CLEAR COMPLETED TASKS ----------------
@tasks_bp.route('/clear-completed', methods=['POST'])
@login_required
def clear_completed():
    completed_tasks = Task.query.filter_by(user_id=current_user.id, status='completed').all()

    try:
        for task in completed_tasks:
            db.session.delete(task)
        db.session.commit()
        flash(f'{len(completed_tasks)} completed tasks cleared', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while clearing tasks', 'danger')

    return redirect(url_for('tasks.dashboard'))

# ---------------- ADD CATEGORY ----------------
@tasks_bp.route('/category/add', methods=['POST'])
@login_required
def add_category():
    name = request.form.get('name')
    color = request.form.get('color', '#007bff')

    if not name:
        flash('Category name is required', 'danger')
        return redirect(url_for('tasks.dashboard'))

    existing = TaskCategory.query.filter_by(name=name, user_id=current_user.id).first()
    if existing:
        flash('Category already exists', 'danger')
        return redirect(url_for('tasks.dashboard'))

    new_category = TaskCategory(name=name, color=color, user_id=current_user.id)

    try:
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while adding the category', 'danger')

    return redirect(url_for('tasks.dashboard'))

# ---------------- DELETE CATEGORY ----------------
@tasks_bp.route('/category/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = TaskCategory.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()

    tasks_with_category = Task.query.filter_by(category_id=category_id).all()
    for task in tasks_with_category:
        task.category = None

    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting the category', 'danger')

    return redirect(url_for('tasks.dashboard'))
