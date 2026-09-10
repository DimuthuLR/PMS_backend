from flask import Blueprint, request, jsonify
from ..models.care_log import CareLog
from ..models.batch import Batch
from .. import db
from ..utils.auth import token_required
from datetime import datetime

care_bp = Blueprint('care', __name__)

def _parse_date(value):
    """Convert 'YYYY-MM-DD' string to a Python date object."""
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()

@care_bp.route('', methods=['GET'])
@token_required
def get_care_logs(current_user):
    """List all care logs (optional ?batch_id=1 filter)"""
    batch_id = request.args.get('batch_id')
    query = CareLog.query
    if batch_id:
        query = query.filter_by(batch_id=batch_id)
    logs = query.order_by(CareLog.date.desc()).all()
    return jsonify([log.to_dict() for log in logs]), 200

@care_bp.route('/<int:log_id>', methods=['GET'])
@token_required
def get_care_log(current_user, log_id):
    log = CareLog.query.get(log_id)
    if not log:
        return jsonify({'message': 'Care log not found'}), 404
    return jsonify(log.to_dict()), 200

@care_bp.route('', methods=['POST'])
@token_required
def create_care_log(current_user):
    data = request.get_json()

    # Validate
    if not data.get('batch_id'):
        return jsonify({'message': 'batch_id is required'}), 400
    if not data.get('type'):
        return jsonify({'message': 'type is required (organic/chemical)'}), 400
    if not data.get('product'):
        return jsonify({'message': 'product is required'}), 400
    if not data.get('date'):
        return jsonify({'message': 'date is required (YYYY-MM-DD)'}), 400

    if not Batch.query.get(data['batch_id']):
        return jsonify({'message': 'Batch not found'}), 404

    try:
        log_date = _parse_date(data['date'])
        next_due = _parse_date(data.get('next_due'))
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    log = CareLog(
        batch_id=data['batch_id'],
        type=data['type'],
        product=data['product'],
        quantity=data.get('quantity'),
        method=data.get('method'),
        cost=data.get('cost', 0.0),
        date=log_date,
        next_due=next_due,
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(log.to_dict()), 201

@care_bp.route('/<int:log_id>', methods=['PUT'])
@token_required
def update_care_log(current_user, log_id):
    log = CareLog.query.get(log_id)
    if not log:
        return jsonify({'message': 'Care log not found'}), 404

    data = request.get_json()
    log.type = data.get('type', log.type)
    log.product = data.get('product', log.product)
    log.quantity = data.get('quantity', log.quantity)
    log.method = data.get('method', log.method)
    log.cost = data.get('cost', log.cost)

    if data.get('batch_id'):
        log.batch_id = data['batch_id']
    if data.get('date'):
        try:
            log.date = _parse_date(data['date'])
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400
    if 'next_due' in data:
        try:
            log.next_due = _parse_date(data['next_due'])
        except ValueError:
            return jsonify({'message': 'Invalid next_due format'}), 400

    db.session.commit()
    return jsonify(log.to_dict()), 200

@care_bp.route('/<int:log_id>', methods=['DELETE'])
@token_required
def delete_care_log(current_user, log_id):
    log = CareLog.query.get(log_id)
    if not log:
        return jsonify({'message': 'Care log not found'}), 404
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Care log deleted'}), 200