from datetime import datetime
from ..models.alert import Alert
from ..models.sensor import Sensor
from ..models.tank import Tank
from ..models.actuator import Actuator
from .. import db


def generate_alerts():
    """
    Inspect current system state and create alerts for anomalies.
    Returns a summary of what was created.
    """
    created = []
    sensor = Sensor.query.first()
    tank = Tank.query.first()

    # ---- Sensor-based alerts ----
    if sensor:
        # Soil moisture low (needs irrigation)
        if sensor.soil_moisture < 30:
            created.append(_make_alert(
                type='warning',
                message=f'Soil moisture is low ({sensor.soil_moisture}%). Consider irrigation.',
            ))

        # Soil moisture critically low
        if sensor.soil_moisture < 15:
            created.append(_make_alert(
                type='danger',
                message=f'CRITICAL: Soil moisture at {sensor.soil_moisture}%. Immediate irrigation required.',
            ))

        # Temperature extremes
        if sensor.temperature > 35:
            created.append(_make_alert(
                type='warning',
                message=f'High temperature alert: {sensor.temperature}°C. Watch for heat stress.',
            ))
        elif sensor.temperature < 10:
            created.append(_make_alert(
                type='warning',
                message=f'Low temperature alert: {sensor.temperature}°C. Risk of cold damage.',
            ))

        # Humidity extremes
        if sensor.humidity > 90:
            created.append(_make_alert(
                type='warning',
                message=f'High humidity ({sensor.humidity}%). Increased fungal disease risk.',
            ))

    # ---- Tank-based alerts ----
    if tank:
        if tank.level < tank.low_level_threshold:
            created.append(_make_alert(
                type='danger',
                message=f'Tank level critical ({tank.level}L). Refill required.',
            ))
        elif tank.level < tank.low_level_threshold * 1.5:
            created.append(_make_alert(
                type='warning',
                message=f'Tank level low ({tank.level}L). Plan a refill soon.',
            ))

    # ---- Actuator-based alerts ----
    auto_actuators = Actuator.query.filter_by(mode='auto').count()
    if sensor and sensor.soil_moisture < 30 and auto_actuators == 0:
        created.append(_make_alert(
            type='info',
            message='Soil is dry but no actuators are in auto mode. Enable auto-irrigation.',
        ))

    db.session.commit()
    return {
        'created_count': len(created),
        'alerts': [a.to_dict() for a in created],
    }


def _make_alert(type, message):
    """Helper: create a new alert row."""
    alert = Alert(
        type=type,
        message=message,
        timestamp=datetime.utcnow(),
    )
    db.session.add(alert)
    return alert