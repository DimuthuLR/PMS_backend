from flask import Blueprint, request, jsonify
from ..models.pest import Pest
from ..models.batch import Batch
from .. import db
from ..utils.auth import token_required
from datetime import datetime

pest_bp = Blueprint('pest', __name__)

def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()

@pest_bp.route('', methods=['GET'])
@token_required
def get_pests(current_user):
    batch_id = request.args.get('batch_id')
    query = Pest.query
    if batch_id:
        query = query.filter_by(batch_id=batch_id)
    items = query.order_by(Pest.date.desc()).all()
    return jsonify([p.to_dict() for p in items]), 200

@pest_bp.route('/<int:pest_id>', methods=['GET'])
@token_required
def get_pest(current_user, pest_id):
    item = Pest.query.get(pest_id)
    if not item:
        return jsonify({'message': 'Pest record not found'}), 404
    return jsonify(item.to_dict()), 200

@pest_bp.route('', methods=['POST'])
@token_required
def create_pest(current_user):
    data = request.get_json()
    if not data.get('batch_id'):
        return jsonify({'message': 'batch_id is required'}), 400
    if not data.get('symptom'):
        return jsonify({'message': 'symptom is required'}), 400
    if not data.get('date'):
        return jsonify({'message': 'date is required (YYYY-MM-DD)'}), 400
    if not Batch.query.get(data['batch_id']):
        return jsonify({'message': 'Batch not found'}), 404

    try:
        p_date = _parse_date(data['date'])
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    item = Pest(
        batch_id=data['batch_id'],
        symptom=data['symptom'],
        severity=data.get('severity', 1),
        date=p_date,
        image_url=data.get('image_url'),
        resolved=data.get('resolved', False),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@pest_bp.route('/<int:pest_id>', methods=['PUT'])
@token_required
def update_pest(current_user, pest_id):
    item = Pest.query.get(pest_id)
    if not item:
        return jsonify({'message': 'Pest record not found'}), 404

    data = request.get_json()
    item.batch_id = data.get('batch_id', item.batch_id)
    item.symptom = data.get('symptom', item.symptom)
    item.severity = data.get('severity', item.severity)
    item.image_url = data.get('image_url', item.image_url)
    item.resolved = data.get('resolved', item.resolved)

    if data.get('date'):
        try:
            item.date = _parse_date(data['date'])
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400

    db.session.commit()
    return jsonify(item.to_dict()), 200

@pest_bp.route('/<int:pest_id>', methods=['DELETE'])
@token_required
def delete_pest(current_user, pest_id):
    item = Pest.query.get(pest_id)
    if not item:
        return jsonify({'message': 'Pest record not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Pest record deleted'}), 200