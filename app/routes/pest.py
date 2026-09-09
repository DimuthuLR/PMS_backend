from flask import Blueprint, request, jsonify
from ..models import Pest, Batch
from .. import db
from ..utils.auth import token_required

pest_bp = Blueprint('pest', __name__)

@pest_bp.route('', methods=['GET'])
@token_required
def get_pests():
    batch_id = request.args.get('batch_id')
    if batch_id:
        pests = Pest.query.filter_by(batch_id=batch_id).all()
    else:
        pests = Pest.query.all()
    return jsonify([p.to_dict() for p in pests]), 200

@pest_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_pest(id):
    pest = Pest.query.get(id)
    if not pest:
        return jsonify({'error': 'Pest record not found'}), 404
    return jsonify(pest.to_dict()), 200

@pest_bp.route('', methods=['POST'])
@token_required
def create_pest():
    data = request.get_json()
    batch = Batch.query.get(data.get('batchId'))
    if not batch:
        return jsonify({'error': 'Batch not found'}), 404
    pest = Pest(
        batch_id=data.get('batchId'),
        symptom=data.get('symptom'),
        severity=data.get('severity', 3),
        date=data.get('date'),
        image_url=data.get('imageUrl'),
        resolved=data.get('resolved', False)
    )
    db.session.add(pest)
    db.session.commit()
    return jsonify(pest.to_dict()), 201

@pest_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_pest(id):
    pest = Pest.query.get(id)
    if not pest:
        return jsonify({'error': 'Pest record not found'}), 404
    data = request.get_json()
    pest.symptom = data.get('symptom', pest.symptom)
    pest.severity = data.get('severity', pest.severity)
    pest.date = data.get('date', pest.date)
    pest.image_url = data.get('imageUrl', pest.image_url)
    pest.resolved = data.get('resolved', pest.resolved)
    db.session.commit()
    return jsonify(pest.to_dict()), 200

@pest_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_pest(id):
    pest = Pest.query.get(id)
    if not pest:
        return jsonify({'error': 'Pest record not found'}), 404
    db.session.delete(pest)
    db.session.commit()
    return jsonify({'message': 'Pest record deleted'}), 200