from flask import Blueprint, request, jsonify
from ..models.task import Task
from ..models.batch import Batch
from .. import db
from ..utils.auth import token_required
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()

@tasks_bp.route('', methods=['GET'])
@token_required
def get_tasks(current_user):
    batch_id = request.args.get('batch_id')
    status = request.args.get('status')
    query = Task.query
    if batch_id:
        query = query.filter_by(batch_id=batch_id)
    if status:
        query = query.filter_by(status=status)
    items = query.all()
    return jsonify([t.to_dict() for t in items]), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    item = Task.query.get(task_id)
    if not item:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify(item.to_dict()), 200

@tasks_bp.route('', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    if not data.get('batch_id'):
        return jsonify({'message': 'batch_id is required'}), 400
    if not data.get('title'):
        return jsonify({'message': 'title is required'}), 400
    if not Batch.query.get(data['batch_id']):
        return jsonify({'message': 'Batch not found'}), 404

    deadline = None
    if data.get('deadline'):
        try:
            deadline = _parse_date(data['deadline'])
        except ValueError:
            return jsonify({'message': 'Invalid deadline format'}), 400

    item = Task(
        batch_id=data['batch_id'],
        title=data['title'],
        assigned_to=data.get('assigned_to'),
        deadline=deadline,
        status=data.get('status', 'pending'),
        hours_logged=data.get('hours_logged', 0.0),
        labor_cost=data.get('labor_cost', 0.0),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    item = Task.query.get(task_id)
    if not item:
        return jsonify({'message': 'Task not found'}), 404

    data = request.get_json()
    item.batch_id = data.get('batch_id', item.batch_id)
    item.title = data.get('title', item.title)
    item.assigned_to = data.get('assigned_to', item.assigned_to)
    item.status = data.get('status', item.status)
    item.hours_logged = data.get('hours_logged', item.hours_logged)
    item.labor_cost = data.get('labor_cost', item.labor_cost)

    if data.get('deadline'):
        try:
            item.deadline = _parse_date(data['deadline'])
        except ValueError:
            return jsonify({'message': 'Invalid deadline format'}), 400

    db.session.commit()
    return jsonify(item.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    item = Task.query.get(task_id)
    if not item:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200