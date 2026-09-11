from flask import Blueprint, jsonify
from ..models.sensor import Sensor
from ..models.tank import Tank
from ..models.actuator import Actuator
from ..models.weather import Weather
from ..models.alert import Alert
from ..models.batch import Batch
from ..utils.auth import token_required
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('', methods=['GET'])
@token_required
def get_dashboard(current_user):
    """Aggregated dashboard summary in a single response."""

    sensor = Sensor.query.first()
    tank = Tank.query.first()
    weather = Weather.query.first()

    # Actuator counts
    total_actuators = Actuator.query.count()
    active_valves = Actuator.query.filter_by(status='on').count()
    auto_actuators = Actuator.query.filter_by(mode='auto').count()

    # Alert counts
    unread_alerts = Alert.query.filter_by(read=False).count()
    danger_alerts = Alert.query.filter_by(type='danger', read=False).count()

    # Batch counts
    total_batches = Batch.query.count()
    active_batches = Batch.query.filter(
        Batch.stage.notin_(['Harvested', 'Decommissioned'])
    ).count()

    # Determine system status
    status = 'Operational'
    if danger_alerts > 0:
        status = 'Critical'
    elif unread_alerts > 0:
        status = 'Warning'

    # Tank safety check
    tank_low = False
    if tank and tank.level < tank.low_level_threshold:
        tank_low = True
        if status == 'Operational':
            status = 'Warning'

    return jsonify({
        'system_status': status,
        'active_valves': active_valves,
        'total_actuators': total_actuators,
        'auto_actuators': auto_actuators,
        'temperature': sensor.temperature if sensor else None,
        'humidity': sensor.humidity if sensor else None,
        'soil_moisture': sensor.soil_moisture if sensor else None,
        'tank_level': tank.level if tank else None,
        'tank_capacity': tank.capacity if tank else None,
        'tank_low': tank_low,
        'weather_condition': weather.condition if weather else None,
        'weather_temp': weather.temp if weather else None,
        'unread_alerts': unread_alerts,
        'danger_alerts': danger_alerts,
        'total_batches': total_batches,
        'active_batches': active_batches,
        'timestamp': datetime.utcnow().isoformat(),
    }), 200