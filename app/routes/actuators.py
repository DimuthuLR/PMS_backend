from flask import Blueprint, request, jsonify
from ..models.actuator import Actuator
from .. import db
from ..utils.auth import token_required
from ..services.irrigation import run_auto_irrigation
from datetime import datetime

actuators_bp = Blueprint('actuators', __name__)

@actuators_bp.route('', methods=['GET'])
@token_required
def get_actuators(current_user):
    items = Actuator.query.all()
    return jsonify([a.to_dict() for a in items]), 200

@actuators_bp.route('/<int:actuator_id>', methods=['GET'])
@token_required
def get_actuator(current_user, actuator_id):
    item = Actuator.query.get(actuator_id)
    if not item:
        return jsonify({'message': 'Actuator not found'}), 404
    return jsonify(item.to_dict()), 200

@actuators_bp.route('', methods=['POST'])
@token_required
def create_actuator(current_user):
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'message': 'name is required'}), 400

    item = Actuator(
        name=data['name'],
        type=data.get('type', 'valve'),
        zone=data.get('zone'),
        status=data.get('status', 'off'),
        mode=data.get('mode', 'manual'),
        auto_threshold=data.get('auto_threshold', 30.0),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@actuators_bp.route('/<int:actuator_id>', methods=['PUT'])
@token_required
def update_actuator(current_user, actuator_id):
    item = Actuator.query.get(actuator_id)
    if not item:
        return jsonify({'message': 'Actuator not found'}), 404

    data = request.get_json()
    item.name = data.get('name', item.name)
    item.type = data.get('type', item.type)
    item.zone = data.get('zone', item.zone)
    item.status = data.get('status', item.status)
    item.mode = data.get('mode', item.mode)
    item.auto_threshold = data.get('auto_threshold', item.auto_threshold)

    db.session.commit()
    return jsonify(item.to_dict()), 200

@actuators_bp.route('/<int:actuator_id>', methods=['DELETE'])
@token_required
def delete_actuator(current_user, actuator_id):
    item = Actuator.query.get(actuator_id)
    if not item:
        return jsonify({'message': 'Actuator not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Actuator deleted'}), 200

@actuators_bp.route('/<int:actuator_id>/toggle', methods=['POST'])
@token_required
def toggle_actuator(current_user, actuator_id):
    """Toggle actuator ON <-> OFF"""
    item = Actuator.query.get(actuator_id)
    if not item:
        return jsonify({'message': 'Actuator not found'}), 404

    item.status = 'off' if item.status == 'on' else 'on'
    item.last_toggled = datetime.utcnow()
    db.session.commit()
    return jsonify(item.to_dict()), 200

@actuators_bp.route('/run-auto', methods=['POST'])
@token_required
def run_auto(current_user):
    """Run auto-irrigation logic (admin/manager only in future)."""
    result = run_auto_irrigation()
    return jsonify(result), 200