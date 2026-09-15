from flask import Blueprint, request, jsonify
from ..models.sensor import Sensor
from .. import db
from ..utils.auth import token_required
from ..socketio import socketio
from ..services.sensor_simulation import (
    get_or_create_sensor,
    simulate_sensor_reading,
    emit_dashboard_refresh,
)
from datetime import datetime

sensors_bp = Blueprint('sensors', __name__)


@sensors_bp.route('', methods=['GET'])
@token_required
def get_sensor(current_user):
    sensor = get_or_create_sensor()
    return jsonify(sensor.to_dict()), 200


@sensors_bp.route('', methods=['PUT'])
@token_required
def update_sensor(current_user):
    sensor = get_or_create_sensor()
    data = request.get_json()
    sensor.temperature = data.get('temperature', sensor.temperature)
    sensor.humidity = data.get('humidity', sensor.humidity)
    sensor.soil_moisture = data.get('soil_moisture', sensor.soil_moisture)
    sensor.last_updated = datetime.utcnow()
    db.session.commit()

    # ✅ Emit real-time updates
    socketio.emit('sensor:update', sensor.to_dict())
    emit_dashboard_refresh('sensor updated')

    return jsonify(sensor.to_dict()), 200


@sensors_bp.route('/simulate', methods=['POST'])
@token_required
def simulate_sensor(current_user):
    """Generate a new simulated sensor reading."""
    sensor = get_or_create_sensor()
    new_data = simulate_sensor_reading(previous=sensor)
    sensor.temperature = new_data['temperature']
    sensor.humidity = new_data['humidity']
    sensor.soil_moisture = new_data['soil_moisture']
    sensor.last_updated = datetime.utcnow()
    db.session.commit()

    # ✅ Emit
    socketio.emit('sensor:update', sensor.to_dict())
    emit_dashboard_refresh('sensor simulated')

    return jsonify(sensor.to_dict()), 200