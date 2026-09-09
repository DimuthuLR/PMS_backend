from flask import Blueprint, request, jsonify
from ..models import CareLog, Batch
from .. import db
from ..utils.auth import token_required


care_bp = Blueprint('care', __name__)

@care_bp.route('', methods=['GET'])
@token_required
def get_care_logs():
    """Get all care logs (optionally filter by batch_id)"""
    batch_id = request.args.get('batch_id')
    if batch_id:
        logs = CareLog.query.filter_by(batch_id=batch_id).all()
    else:
        logs = CareLog.query.all()
    return jsonify([log.to_dict() for log in logs]), 200

@care_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_care_log(id):
    log = CareLog.query.get(id)
    if not log:
        return jsonify({'error': 'Care log not found'}), 404
    return jsonify(log.to_dict()), 200

@care_bp.route('', methods=['POST'])
@token_required
def create_care_log():
    data = request.get_json()
    # Validate batch exists
    batch = Batch.query.get(data.get('batchId'))
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    
    log = CareLog(
        batch_id=data.get('batchId'),
        type=data.get('type', 'organic'),
        product=data.get('product'),
        quantity=data.get('quantity'),
        method=data.get('method'),
        cost=data.get('cost', 0),
        date=data.get('date'),
        next_due=data.get('nextDue')
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(log.to_dict()), 201

@care_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_care_log(id):
    log = CareLog.query.get(id)
    if not log:
        return jsonify({'error': 'Care log not found'}), 404
    
    data = request.get_json()
    log.type = data.get('type', log.type)
    log.product = data.get('product', log.product)
    log.quantity = data.get('quantity', log.quantity)
    log.method = data.get('method', log.method)
    log.cost = data.get('cost', log.cost)
    log.date = data.get('date', log.date)
    log.next_due = data.get('nextDue', log.next_due)
    
    db.session.commit()
    return jsonify(log.to_dict()), 200

@care_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_care_log(id):
    log = CareLog.query.get(id)
    if not log:
        return jsonify({'error': 'Care log not found'}), 404
    
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Care log deleted'}), 200