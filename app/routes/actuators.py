from flask import Blueprint, request, jsonify
from ..models import Actuator
from .. import db
from ..utils.auth import token_required, admin_required, manager_required

actuators_bp = Blueprint('actuators', __name__)

@actuators_bp.route('', methods=['GET'])
@token_required
def get_actuators():
    actuators = Actuator.query.all()
    return jsonify([a.to_dict() for a in actuators]), 200

@actuators_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_actuator(id):
    actuator = Actuator.query.get(id)
    if not actuator:
        return jsonify({'error': 'Actuator not found'}), 404
    return jsonify(actuator.to_dict()), 200

@actuators_bp.route('', methods=['POST'])
@token_required
@admin_required  # Only admin can create
def create_actuator():
    data = request.get_json()
    actuator = Actuator(
        name=data.get('name'),
        type=data.get('type', 'valve'),
        zone=data.get('zone'),
        status='off',
        mode=data.get('mode', 'manual'),
        auto_threshold=data.get('autoThreshold', 40)
    )
    db.session.add(actuator)
    db.session.commit()
    return jsonify(actuator.to_dict()), 201

@actuators_bp.route('/<int:id>', methods=['PUT'])
@token_required
@admin_required
def update_actuator(id):
    actuator = Actuator.query.get(id)
    if not actuator:
        return jsonify({'error': 'Actuator not found'}), 404
    data = request.get_json()
    actuator.name = data.get('name', actuator.name)
    actuator.type = data.get('type', actuator.type)
    actuator.zone = data.get('zone', actuator.zone)
    actuator.status = data.get('status', actuator.status)
    actuator.mode = data.get('mode', actuator.mode)
    actuator.auto_threshold = data.get('autoThreshold', actuator.auto_threshold)
    db.session.commit()
    return jsonify(actuator.to_dict()), 200

@actuators_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_actuator(id):
    actuator = Actuator.query.get(id)
    if not actuator:
        return jsonify({'error': 'Actuator not found'}), 404
    db.session.delete(actuator)
    db.session.commit()
    return jsonify({'message': 'Actuator deleted'}), 200

@actuators_bp.route('/<int:id>/toggle', methods=['POST'])
@token_required
def toggle_actuator(id):
    actuator = Actuator.query.get(id)
    if not actuator:
        return jsonify({'error': 'Actuator not found'}), 404
    # Only admin/manager can toggle, operator can too (we'll let all authenticated)
    actuator.status = 'on' if actuator.status == 'off' else 'off'
    db.session.commit()
    return jsonify(actuator.to_dict()), 200