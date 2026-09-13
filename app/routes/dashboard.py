from flask import Blueprint, jsonify
from datetime import datetime, date
from sqlalchemy import func

from .. import db
from ..models.sensor import Sensor
from ..models.tank import Tank
from ..models.actuator import Actuator
from ..models.weather import Weather
from ..models.alert import Alert
from ..models.batch import Batch
from ..models.harvest import Harvest
from ..models.task import Task
from ..utils.auth import token_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('', methods=['GET'])
@token_required
def get_dashboard(current_user):
    """
    One endpoint to power the entire dashboard.
    Returns: summary metrics + singleton objects + recent alerts.
    """
    today = date.today()

    # ---- Singletons (full objects) ----
    sensor = Sensor.query.first()
    tank = Tank.query.first()
    weather = Weather.query.first()

    # ---- Batch summary ----
    active_batches = Batch.query.filter(
        Batch.stage.notin_(['Harvested', 'Decommissioned'])
    ).count()
    total_plants = db.session.query(
        func.coalesce(func.sum(Batch.initial_count), 0)
    ).scalar()

    # ---- Harvest summary ----
    today_harvest_kg = db.session.query(
        func.coalesce(func.sum(Harvest.weight_kg), 0)
    ).filter(Harvest.date == today).scalar()

    # ---- Task summary ----
    pending_tasks = Task.query.filter_by(status='pending').count()
    overdue_tasks = Task.query.filter(
        Task.deadline < today,
        Task.status != 'done',
    ).count()

    # ---- Actuator summary ----
    total_actuators = Actuator.query.count()
    active_valves = Actuator.query.filter_by(type='valve', status='on').count()
    auto_actuators = Actuator.query.filter_by(mode='auto').count()

    # ---- Alert summary + recent list ----
    unread_alerts_count = Alert.query.filter_by(read=False).count()
    danger_alerts_count = Alert.query.filter_by(type='danger', read=False).count()
    recent_alerts = (
        Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()
    )

    # ---- System status ----
    status = 'Operational'
    tank_low = False

    if tank and tank.level < tank.low_level_threshold:
        tank_low = True
        status = 'Warning'

    if danger_alerts_count > 0:
        status = 'Critical'
    elif unread_alerts_count > 0 and status == 'Operational':
        status = 'Warning'

    return jsonify({
        # System status
        'system_status': status,

        # Metrics
        'active_batches': active_batches,
        'total_plants': int(total_plants),
        'today_harvest_kg': float(today_harvest_kg or 0),
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,

        # Actuator summary
        'total_actuators': total_actuators,
        'active_valves': active_valves,
        'auto_actuators': auto_actuators,

        # Alert summary + recent list
        'unread_alerts': unread_alerts_count,
        'danger_alerts': danger_alerts_count,
        'alerts': [a.to_dict() for a in recent_alerts],

        # Singletons
        'sensors': sensor.to_dict() if sensor else None,
        'weather': weather.to_dict() if weather else None,
        'tank': tank.to_dict() if tank else None,
        'tank_low': tank_low,

        'timestamp': datetime.utcnow().isoformat(),
    }), 200