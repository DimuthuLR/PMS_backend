from flask import Blueprint, request, jsonify
from ..models.financial import Financial
from ..models.batch import Batch
from .. import db
from ..utils.auth import token_required, manager_required
from datetime import datetime

financial_bp = Blueprint('financial', __name__)

def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()

@financial_bp.route('', methods=['GET'])
@token_required
def get_financials(current_user):
    batch_id = request.args.get('batch_id')
    query = Financial.query
    if batch_id:
        query = query.filter_by(batch_id=batch_id)
    items = query.order_by(Financial.date.desc()).all()
    return jsonify([f.to_dict() for f in items]), 200

@financial_bp.route('/<int:item_id>', methods=['GET'])
@token_required
def get_financial(current_user, item_id):
    item = Financial.query.get(item_id)
    if not item:
        return jsonify({'message': 'Financial record not found'}), 404
    return jsonify(item.to_dict()), 200

@financial_bp.route('', methods=['POST'])
@token_required
def create_financial(current_user):
    data = request.get_json()
    if not data.get('batch_id'):
        return jsonify({'message': 'batch_id is required'}), 400
    if not data.get('category'):
        return jsonify({'message': 'category is required'}), 400
    if not data.get('date'):
        return jsonify({'message': 'date is required (YYYY-MM-DD)'}), 400
    if not Batch.query.get(data['batch_id']):
        return jsonify({'message': 'Batch not found'}), 404

    try:
        item_date = _parse_date(data['date'])
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    item = Financial(
        batch_id=data['batch_id'],
        category=data['category'],
        cost_amount=data.get('cost_amount', 0.0),
        date=item_date,
        description=data.get('description'),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@financial_bp.route('/<int:item_id>', methods=['PUT'])
@token_required
def update_financial(current_user, item_id):
    item = Financial.query.get(item_id)
    if not item:
        return jsonify({'message': 'Financial record not found'}), 404

    data = request.get_json()
    item.batch_id = data.get('batch_id', item.batch_id)
    item.category = data.get('category', item.category)
    item.cost_amount = data.get('cost_amount', item.cost_amount)
    item.description = data.get('description', item.description)

    if data.get('date'):
        try:
            item.date = _parse_date(data['date'])
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400

    db.session.commit()
    return jsonify(item.to_dict()), 200

@financial_bp.route('/<int:item_id>', methods=['DELETE'])
@token_required
def delete_financial(current_user, item_id):
    item = Financial.query.get(item_id)
    if not item:
        return jsonify({'message': 'Financial record not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Financial record deleted'}), 200