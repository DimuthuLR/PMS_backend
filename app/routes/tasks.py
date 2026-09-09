from flask import Blueprint, request, jsonify
from ..models import Task, Batch
from .. import db
from ..utils.auth import token_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
@token_required
def get_tasks():
    batch_id = request.args.get('batch_id')
    if batch_id:
        tasks = Task.query.filter_by(batch_id=batch_id).all()
    else:
        tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks]), 200

@tasks_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200

@tasks_bp.route('', methods=['POST'])
@token_required
def create_task():
    data = request.get_json()
    batch = Batch.query.get(data.get('batchId'))
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    task = Task(
        batch_id=data.get('batchId'),
        title=data.get('title'),
        assigned_to=data.get('assignedTo'),
        deadline=data.get('deadline'),
        status=data.get('status', 'pending'),
        hours_logged=data.get('hoursLogged', 0),
        labor_cost=data.get('laborCost', 0)
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@tasks_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.assigned_to = data.get('assignedTo', task.assigned_to)
    task.deadline = data.get('deadline', task.deadline)
    task.status = data.get('status', task.status)
    task.hours_logged = data.get('hoursLogged', task.hours_logged)
    task.labor_cost = data.get('laborCost', task.labor_cost)
    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200