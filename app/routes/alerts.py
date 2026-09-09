from flask import Blueprint, request, jsonify
from ..models import Alert, Sensor, Tank
from .. import db
from ..utils.auth import token_required
from datetime import datetime

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('', methods=['GET'])
@token_required
def get_alerts():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()
    return jsonify([a.to_dict() for a in alerts]), 200

@alerts_bp.route('/generate', methods=['POST'])
@token_required
def generate_alerts():
    # Generate alerts based on sensor/tank data
    sensor = Sensor.query.first()
    tank = Tank.query.first()
    new_alerts = []
    
    if sensor and sensor.temperature > 35:
        alert = Alert(type='danger', message=f"High temperature: {sensor.temperature}°C")
        db.session.add(alert)
        new_alerts.append(alert)
    if sensor and sensor.soil_moisture < 30:
        alert = Alert(type='warning', message=f"Low soil moisture: {sensor.soil_moisture}%")
        db.session.add(alert)
        new_alerts.append(alert)
    if tank and tank.level < tank.low_level_threshold:
        alert = Alert(type='danger', message=f"Tank level low: {tank.level}%")
        db.session.add(alert)
        new_alerts.append(alert)
    
    db.session.commit()
    return jsonify([a.to_dict() for a in new_alerts]), 201

@alerts_bp.route('/<int:id>/read', methods=['PUT'])
@token_required
def mark_read(id):
    alert = Alert.query.get(id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    alert.read = True
    db.session.commit()
    return jsonify(alert.to_dict()), 200