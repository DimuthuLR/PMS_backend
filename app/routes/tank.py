from flask import Blueprint, request, jsonify
from ..models.tank import Tank
from .. import db
from ..utils.auth import token_required
from ..services.sensor_simulation import get_or_create_weather

tank_bp = Blueprint('tank', __name__)

@tank_bp.route('', methods=['GET'])
@token_required
def get_tank(current_user):
    tank = Tank.query.first()
    if not tank:
        tank = Tank(level=500.0, capacity=1000.0)
        db.session.add(tank)
        db.session.commit()
    return jsonify(tank.to_dict()), 200

@tank_bp.route('', methods=['PUT'])
@token_required
def update_tank(current_user):
    tank = Tank.query.first()
    if not tank:
        tank = Tank()
        db.session.add(tank)

    data = request.get_json()
    tank.level = data.get('level', tank.level)
    tank.capacity = data.get('capacity', tank.capacity)
    tank.pump_status = data.get('pump_status', tank.pump_status)
    tank.auto_mode = data.get('auto_mode', tank.auto_mode)
    tank.low_level_threshold = data.get('low_level_threshold', tank.low_level_threshold)
    tank.fill_level_threshold = data.get('fill_level_threshold', tank.fill_level_threshold)

    db.session.commit()
    return jsonify(tank.to_dict()), 200

@tank_bp.route('/toggle-pump', methods=['POST'])
@token_required
def toggle_pump(current_user):
    tank = Tank.query.first()
    if not tank:
        return jsonify({'message': 'Tank not initialized'}), 404

    tank.pump_status = 'off' if tank.pump_status == 'on' else 'on'
    db.session.commit()
    return jsonify(tank.to_dict()), 200