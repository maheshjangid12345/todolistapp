from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Task, TaskCategory
from datetime import datetime
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get all tasks for the current user"""
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    category_filter = request.args.get('category_id')
    
    query = Task.query.filter_by(user_id=current_user.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    """Get a specific task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    return jsonify(task.to_dict())

@api_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Parse due date
    due_date = None
    if data.get('due_date'):
        try:
            # Convert YYYY-MM-DD to datetime object
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid due date format'}), 400
    
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        due_date=due_date,
        user_id=current_user.id
    )
    
    if data.get('category_id'):
        category = TaskCategory.query.filter_by(id=data['category_id'], user_id=current_user.id).first()
        if category:
            new_task.category = category
    
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create task'}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update a task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'priority' in data and data['priority'] in Task.PRIORITY_CHOICES:
        task.priority = data['priority']
    if 'status' in data and data['status'] in Task.STATUS_CHOICES:
        task.status = data['status']
        if data['status'] == 'completed' and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif data['status'] != 'completed':
            task.completed_at = None
    
    # Parse due date
    if 'due_date' in data:
        if data['due_date']:
            try:
                # Convert YYYY-MM-DD to datetime object
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Invalid due date format'}), 400
        else:
            task.due_date = None
    
    # Update category
    if 'category_id' in data:
        if data['category_id']:
            category = TaskCategory.query.filter_by(id=data['category_id'], user_id=current_user.id).first()
            task.category = category if category else None
        else:
            task.category = None
    
    try:
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete task'}), 500

@api_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task_status(task_id):
    """Toggle task status"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    # Cycle through statuses
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
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500

@api_bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    """Get all categories for the current user"""
    categories = TaskCategory.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'color': cat.color,
        'created_at': cat.created_at.isoformat()
    } for cat in categories])

@api_bp.route('/categories', methods=['POST'])
@login_required
def create_category():
    """Create a new category"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Check if category already exists
    existing = TaskCategory.query.filter_by(name=data['name'], user_id=current_user.id).first()
    if existing:
        return jsonify({'error': 'Category already exists'}), 400
    
    new_category = TaskCategory(
        name=data['name'],
        color=data.get('color', '#007bff'),
        user_id=current_user.id
    )
    
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({
            'id': new_category.id,
            'name': new_category.name,
            'color': new_category.color,
            'created_at': new_category.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create category'}), 500

@api_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get task statistics for the current user"""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    total_tasks = len(tasks)
    pending_tasks = len([t for t in tasks if t.status == 'pending'])
    in_progress_tasks = len([t for t in tasks if t.status == 'in_progress'])
    completed_tasks = len([t for t in tasks if t.status == 'completed'])
    
    # Overdue tasks
    overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != 'completed'])
    
    # Priority distribution
    priority_stats = {}
    for priority in Task.PRIORITY_CHOICES:
        priority_stats[priority] = len([t for t in tasks if t.priority == priority])
    
    return jsonify({
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'priority_distribution': priority_stats
    })
