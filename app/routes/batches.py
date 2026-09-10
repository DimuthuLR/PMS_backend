from flask import Blueprint, request, jsonify
from ..models.batch import Batch
from ..models.plot import Plot
from .. import db
from ..utils.auth import token_required
from datetime import datetime

batches_bp = Blueprint('batches', __name__)

@batches_bp.route('', methods=['GET'])
@token_required
def get_batches(current_user):
    """List all batches (can filter by plot: /api/batches?plot_id=1)"""
    plot_id = request.args.get('plot_id')
    query = Batch.query
    if plot_id:
        query = query.filter_by(plot_id=plot_id)
    batches = query.all()
    return jsonify([b.to_dict() for b in batches]), 200

@batches_bp.route('/<int:batch_id>', methods=['GET'])
@token_required
def get_batch(current_user, batch_id):
    """Get one batch by ID"""
    batch = Batch.query.get(batch_id)
    if not batch:
        return jsonify({'message': 'Batch not found'}), 404
    return jsonify(batch.to_dict()), 200

@batches_bp.route('', methods=['POST'])
@token_required
def create_batch(current_user):
    """Create a new batch"""
    data = request.get_json()

    # Validate required fields
    if not data.get('plot_id'):
        return jsonify({'message': 'plot_id is required'}), 400
    if not data.get('crop_type'):
        return jsonify({'message': 'crop_type is required'}), 400
    if not data.get('start_date'):
        return jsonify({'message': 'start_date is required (YYYY-MM-DD)'}), 400

    # Make sure the referenced plot exists
    if not Plot.query.get(data['plot_id']):
        return jsonify({'message': 'Plot not found'}), 404

    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    batch = Batch(
        plot_id=data['plot_id'],
        crop_type=data['crop_type'],
        variety=data.get('variety'),
        start_date=start_date,
        initial_count=data.get('initial_count', 0),
        expected_yield=data.get('expected_yield', 0.0),
        stage=data.get('stage', 'Sowing'),
        notes=data.get('notes')
    )
    db.session.add(batch)
    db.session.commit()
    return jsonify(batch.to_dict()), 201

@batches_bp.route('/<int:batch_id>', methods=['PUT'])
@token_required
def update_batch(current_user, batch_id):
    """Update an existing batch"""
    batch = Batch.query.get(batch_id)
    if not batch:
        return jsonify({'message': 'Batch not found'}), 404

    data = request.get_json()
    batch.plot_id = data.get('plot_id', batch.plot_id)
    batch.crop_type = data.get('crop_type', batch.crop_type)
    batch.variety = data.get('variety', batch.variety)
    batch.initial_count = data.get('initial_count', batch.initial_count)
    batch.expected_yield = data.get('expected_yield', batch.expected_yield)
    batch.stage = data.get('stage', batch.stage)
    batch.notes = data.get('notes', batch.notes)

    if data.get('start_date'):
        try:
            batch.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    db.session.commit()
    return jsonify(batch.to_dict()), 200

@batches_bp.route('/<int:batch_id>', methods=['DELETE'])
@token_required
def delete_batch(current_user, batch_id):
    """Delete a batch"""
    batch = Batch.query.get(batch_id)
    if not batch:
        return jsonify({'message': 'Batch not found'}), 404

    db.session.delete(batch)
    db.session.commit()
    return jsonify({'message': 'Batch deleted successfully'}), 200