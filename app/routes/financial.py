from flask import Blueprint, request, jsonify
from ..models import Financial, Batch
from .. import db
from ..utils.auth import token_required, manager_required

financial_bp = Blueprint('financial', __name__)

@financial_bp.route('', methods=['GET'])
@token_required
@manager_required   # Only admin and manager
def get_financials():
    batch_id = request.args.get('batch_id')
    if batch_id:
        records = Financial.query.filter_by(batch_id=batch_id).all()
    else:
        records = Financial.query.all()
    return jsonify([r.to_dict() for r in records]), 200

@financial_bp.route('/<int:id>', methods=['GET'])
@token_required
@manager_required
def get_financial(id):
    record = Financial.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record.to_dict()), 200

@financial_bp.route('', methods=['POST'])
@token_required
@manager_required
def create_financial():
    data = request.get_json()
    batch = Batch.query.get(data.get('batchId'))
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    record = Financial(
        batch_id=data.get('batchId'),
        category=data.get('category'),
        cost_amount=data.get('costAmount', 0),
        date=data.get('date'),
        description=data.get('description')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@financial_bp.route('/<int:id>', methods=['PUT'])
@token_required
@manager_required
def update_financial(id):
    record = Financial.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    data = request.get_json()
    record.category = data.get('category', record.category)
    record.cost_amount = data.get('costAmount', record.cost_amount)
    record.date = data.get('date', record.date)
    record.description = data.get('description', record.description)
    db.session.commit()
    return jsonify(record.to_dict()), 200

@financial_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@manager_required
def delete_financial(id):
    record = Financial.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted'}), 200