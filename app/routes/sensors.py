from flask import Blueprint, request, jsonify
from ..models import Sensor
from .. import db
from ..utils.auth import token_required
from datetime import datetime

sensors_bp = Blueprint('sensors', __name__)

@sensors_bp.route('', methods=['GET'])
@token_required
def get_sensors():
    sensor = Sensor.query.first()
    if not sensor:
        # Create default with mock data
        sensor = Sensor(temperature=24.5, humidity=65, soil_moisture=72)
        db.session.add(sensor)
        db.session.commit()
    return jsonify(sensor.to_dict()), 200

@sensors_bp.route('', methods=['PUT'])
@token_required
def update_sensors():
    sensor = Sensor.query.first()
    if not sensor:
        sensor = Sensor()
        db.session.add(sensor)
    data = request.get_json()
    sensor.temperature = data.get('temperature', sensor.temperature)
    sensor.humidity = data.get('humidity', sensor.humidity)
    sensor.soil_moisture = data.get('soilMoisture', sensor.soil_moisture)
    sensor.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify(sensor.to_dict()), 200