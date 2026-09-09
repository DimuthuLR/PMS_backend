from flask import Blueprint, request, jsonify
from ..models import Batch, Plot
from .. import db
from ..utils.auth import token_required
from datetime import datetime

batches_bp = Blueprint('batches', __name__)

@batches_bp.route('', methods=['GET'])
@token_required
def get_batches():
    batches = Batch.query.all()
    return jsonify([b.to_dict() for b in batches]), 200

@batches_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_batch(id):
    batch = Batch.query.get(id)
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    return jsonify(batch.to_dict()), 200

@batches_bp.route('', methods=['POST'])
@token_required
def create_batch():
    data = request.get_json()
    plot = Plot.query.get(data.get('plotId'))
    if not plot:
        return jsonify({'error': 'Plot not found'}), 404

    # ✅ Parse date string to Python date object
    start_date = None
    if data.get('startDate'):
        try:
            start_date = datetime.strptime(data.get('startDate'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    batch = Batch(
        plot_id=data.get('plotId'),
        crop_type=data.get('cropType'),
        variety=data.get('variety'),
        start_date=start_date,  # now it's a date object
        initial_count=data.get('initialCount', 0),
        expected_yield=data.get('expectedYield', 0),
        stage=data.get('stage', 'Sowing'),
        notes=data.get('notes')
    )
    db.session.add(batch)
    db.session.commit()
    return jsonify(batch.to_dict()), 201

@batches_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_batch(id):
    batch = Batch.query.get(id)
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    data = request.get_json()
    
    if 'plotId' in data:
        batch.plot_id = data['plotId']
    if 'cropType' in data:
        batch.crop_type = data['cropType']
    if 'variety' in data:
        batch.variety = data['variety']
    if 'startDate' in data:
        try:
            batch.start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    if 'initialCount' in data:
        batch.initial_count = data['initialCount']
    if 'expectedYield' in data:
        batch.expected_yield = data['expectedYield']
    if 'stage' in data:
        batch.stage = data['stage']
    if 'notes' in data:
        batch.notes = data['notes']
    
    db.session.commit()
    return jsonify(batch.to_dict()), 200

@batches_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_batch(id):
    batch = Batch.query.get(id)
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    db.session.delete(batch)
    db.session.commit()
    return jsonify({'message': 'Batch deleted'}), 200

@batches_bp.route('/plot/<int:plot_id>', methods=['GET'])
@token_required
def get_batches_by_plot(plot_id):
    batches = Batch.query.filter_by(plot_id=plot_id).all()
    return jsonify([b.to_dict() for b in batches]), 200