from flask import Blueprint, request, jsonify
from ..models import Tank
from .. import db
from ..utils.auth import token_required

tank_bp = Blueprint('tank', __name__)

@tank_bp.route('', methods=['GET'])
@token_required
def get_tank():
    tank = Tank.query.first()
    if not tank:
        # Create default if none exists
        tank = Tank(level=65, capacity=1000, pump_status='off', auto_mode=True, low_level_threshold=20, fill_level_threshold=80)
        db.session.add(tank)
        db.session.commit()
    return jsonify(tank.to_dict()), 200

@tank_bp.route('', methods=['PUT'])
@token_required
def update_tank():
    tank = Tank.query.first()
    if not tank:
        return jsonify({'error': 'Tank not found'}), 404
    data = request.get_json()
    tank.level = data.get('level', tank.level)
    tank.capacity = data.get('capacity', tank.capacity)
    tank.pump_status = data.get('pumpStatus', tank.pump_status)
    tank.auto_mode = data.get('autoMode', tank.auto_mode)
    tank.low_level_threshold = data.get('lowLevelThreshold', tank.low_level_threshold)
    tank.fill_level_threshold = data.get('fillLevelThreshold', tank.fill_level_threshold)
    db.session.commit()
    return jsonify(tank.to_dict()), 200

@tank_bp.route('/toggle-pump', methods=['POST'])
@token_required
def toggle_pump():
    tank = Tank.query.first()
    if not tank:
        return jsonify({'error': 'Tank not found'}), 404
    tank.pump_status = 'on' if tank.pump_status == 'off' else 'off'
    db.session.commit()
    return jsonify(tank.to_dict()), 200