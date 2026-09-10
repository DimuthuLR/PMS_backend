from flask import Blueprint, request, jsonify
from ..models.harvest import Harvest
from ..models.batch import Batch
from .. import db
from ..utils.auth import token_required
from datetime import datetime
from sqlalchemy import func

harvest_bp = Blueprint('harvest', __name__)

def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').date()

@harvest_bp.route('', methods=['GET'])
@token_required
def get_harvests(current_user):
    """List all harvests (optional ?batch_id=1 filter)"""
    batch_id = request.args.get('batch_id')
    query = Harvest.query
    if batch_id:
        query = query.filter_by(batch_id=batch_id)
    harvests = query.order_by(Harvest.date.desc()).all()
    return jsonify([h.to_dict() for h in harvests]), 200

@harvest_bp.route('/summary', methods=['GET'])
@token_required
def get_harvest_summary(current_user):
    """
    Returns aggregate yield + revenue per batch.
    Query: ?batch_id=1 (optional, else returns all batches)
    """
    batch_id = request.args.get('batch_id')
    query = db.session.query(
        Harvest.batch_id,
        func.sum(Harvest.weight_kg).label('total_kg'),
        func.sum(Harvest.revenue).label('total_revenue'),
        func.count(Harvest.id).label('harvest_count'),
    )
    if batch_id:
        query = query.filter(Harvest.batch_id == batch_id)
    rows = query.group_by(Harvest.batch_id).all()

    return jsonify([
        {
            'batch_id': r.batch_id,
            'total_kg': float(r.total_kg or 0),
            'total_revenue': float(r.total_revenue or 0),
            'harvest_count': int(r.harvest_count or 0),
        }
        for r in rows
    ]), 200

@harvest_bp.route('/<int:harvest_id>', methods=['GET'])
@token_required
def get_harvest(current_user, harvest_id):
    h = Harvest.query.get(harvest_id)
    if not h:
        return jsonify({'message': 'Harvest not found'}), 404
    return jsonify(h.to_dict()), 200

@harvest_bp.route('', methods=['POST'])
@token_required
def create_harvest(current_user):
    data = request.get_json()

    if not data.get('batch_id'):
        return jsonify({'message': 'batch_id is required'}), 400
    if not data.get('date'):
        return jsonify({'message': 'date is required (YYYY-MM-DD)'}), 400
    if data.get('weight_kg') is None:
        return jsonify({'message': 'weight_kg is required'}), 400

    if not Batch.query.get(data['batch_id']):
        return jsonify({'message': 'Batch not found'}), 404

    try:
        h_date = _parse_date(data['date'])
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    harvest = Harvest(
        batch_id=data['batch_id'],
        date=h_date,
        weight_kg=data['weight_kg'],
        grade=data.get('grade', 'A'),
        revenue=data.get('revenue', 0.0),
    )
    db.session.add(harvest)
    db.session.commit()
    return jsonify(harvest.to_dict()), 201

@harvest_bp.route('/<int:harvest_id>', methods=['PUT'])
@token_required
def update_harvest(current_user, harvest_id):
    h = Harvest.query.get(harvest_id)
    if not h:
        return jsonify({'message': 'Harvest not found'}), 404

    data = request.get_json()
    h.batch_id = data.get('batch_id', h.batch_id)
    h.weight_kg = data.get('weight_kg', h.weight_kg)
    h.grade = data.get('grade', h.grade)
    h.revenue = data.get('revenue', h.revenue)

    if data.get('date'):
        try:
            h.date = _parse_date(data['date'])
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400

    db.session.commit()
    return jsonify(h.to_dict()), 200

@harvest_bp.route('/<int:harvest_id>', methods=['DELETE'])
@token_required
def delete_harvest(current_user, harvest_id):
    h = Harvest.query.get(harvest_id)
    if not h:
        return jsonify({'message': 'Harvest not found'}), 404
    db.session.delete(h)
    db.session.commit()
    return jsonify({'message': 'Harvest deleted'}), 200