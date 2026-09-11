from datetime import datetime
from ..models.actuator import Actuator
from ..models.tank import Tank
from ..models.sensor import Sensor
from .. import db

def run_auto_irrigation():
    """
    Runs the auto-irrigation logic and returns a summary of actions taken.
    
    Rules:
      1. If tank level < low_level_threshold, turn off all valves (no water).
      2. If tank is fine, for each 'auto' mode actuator:
         - Open valve if soil_moisture < auto_threshold
         - Close valve if soil_moisture >= auto_threshold
    """
    tank = Tank.query.first()
    sensor = Sensor.query.first()
    actuators = Actuator.query.filter_by(mode='auto').all()

    actions = []
    warnings = []

    if not tank or not sensor:
        return {'actions': [], 'warnings': ['No tank or sensor data available']}

    # Rule 1: Tank safety check
    if tank.level < tank.low_level_threshold:
        for actuator in actuators:
            if actuator.status == 'on':
                actuator.status = 'off'
                actuator.last_toggled = datetime.utcnow()
                actions.append({
                    'actuator_id': actuator.id,
                    'name': actuator.name,
                    'action': 'closed',
                    'reason': f'Tank level too low ({tank.level}L < {tank.low_level_threshold}L)',
                })
        warnings.append(f'Low tank level: {tank.level}L')
        db.session.commit()
        return {'actions': actions, 'warnings': warnings}

    # Rule 2: Per-actuator moisture check
    for actuator in actuators:
        if sensor.soil_moisture < actuator.auto_threshold and actuator.status == 'off':
            actuator.status = 'on'
            actuator.last_toggled = datetime.utcnow()
            actions.append({
                'actuator_id': actuator.id,
                'name': actuator.name,
                'action': 'opened',
                'reason': f'Soil moisture {sensor.soil_moisture}% < threshold {actuator.auto_threshold}%',
            })
        elif sensor.soil_moisture >= actuator.auto_threshold and actuator.status == 'on':
            actuator.status = 'off'
            actuator.last_toggled = datetime.utcnow()
            actions.append({
                'actuator_id': actuator.id,
                'name': actuator.name,
                'action': 'closed',
                'reason': f'Soil moisture {sensor.soil_moisture}% >= threshold {actuator.auto_threshold}%',
            })

    db.session.commit()
    return {
        'actions': actions,
        'warnings': warnings,
        'checked': len(actuators),
    }