from flask import Blueprint, request, jsonify
from ..models import Harvest, Batch
from .. import db
from ..utils.auth import token_required

# ✅ This must match the import name
harvest_bp = Blueprint('harvest', __name__)

@harvest_bp.route('', methods=['GET'])
@token_required
def get_harvests():
    batch_id = request.args.get('batch_id')
    if batch_id:
        harvests = Harvest.query.filter_by(batch_id=batch_id).all()
    else:
        harvests = Harvest.query.all()
    return jsonify([h.to_dict() for h in harvests]), 200

@harvest_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_harvest(id):
    harvest = Harvest.query.get(id)
    if not harvest:
        return jsonify({'error': 'Harvest not found'}), 404
    return jsonify(harvest.to_dict()), 200

@harvest_bp.route('', methods=['POST'])
@token_required
def create_harvest():
    data = request.get_json()
    batch = Batch.query.get(data.get('batchId'))
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    harvest = Harvest(
        batch_id=data.get('batchId'),
        date=data.get('date'),
        weight_kg=data.get('weightKg', 0),
        grade=data.get('grade', 'A'),
        revenue=data.get('revenue', 0)
    )
    db.session.add(harvest)
    db.session.commit()
    return jsonify(harvest.to_dict()), 201

@harvest_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_harvest(id):
    harvest = Harvest.query.get(id)
    if not harvest:
        return jsonify({'error': 'Harvest not found'}), 404
    data = request.get_json()
    harvest.date = data.get('date', harvest.date)
    harvest.weight_kg = data.get('weightKg', harvest.weight_kg)
    harvest.grade = data.get('grade', harvest.grade)
    harvest.revenue = data.get('revenue', harvest.revenue)
    db.session.commit()
    return jsonify(harvest.to_dict()), 200

@harvest_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_harvest(id):
    harvest = Harvest.query.get(id)
    if not harvest:
        return jsonify({'error': 'Harvest not found'}), 404
    db.session.delete(harvest)
    db.session.commit()
    return jsonify({'message': 'Harvest deleted'}), 200