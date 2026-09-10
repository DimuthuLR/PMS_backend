from flask import Blueprint, jsonify
from ..utils.auth import token_required
from datetime import datetime, date

stubs_bp = Blueprint('stubs', __name__)

# ---------- TASKS ----------
@stubs_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    return jsonify([]), 200

# ---------- SENSORS ----------
@stubs_bp.route('/sensors', methods=['GET'])
@token_required
def get_sensors(current_user):
    return jsonify({
        'temperature': 24.5,
        'humidity': 62.0,
        'soil_moisture': 45.0,
        'last_updated': datetime.utcnow().isoformat()
    }), 200

# ---------- ALERTS ----------
@stubs_bp.route('/alerts', methods=['GET'])
@token_required
def get_alerts(current_user):
    return jsonify([]), 200

# ---------- WEATHER ----------
@stubs_bp.route('/weather', methods=['GET'])
@token_required
def get_weather(current_user):
    return jsonify({
        'condition': 'Sunny',
        'temp': 27.0,
        'wind_speed': 8.5,
        'humidity': 55.0,
        'forecast': []
    }), 200

# ---------- TANK ----------
@stubs_bp.route('/tank', methods=['GET'])
@token_required
def get_tank(current_user):
    return jsonify({
        'level': 750,
        'capacity': 1000,
        'pump_status': 'off',
        'auto_mode': True,
        'low_level_threshold': 200,
        'fill_level_threshold': 900
    }), 200

# ---------- ACTUATORS ----------
@stubs_bp.route('/actuators', methods=['GET'])
@token_required
def get_actuators(current_user):
    return jsonify([]), 200


# ---------- FINANCIAL ----------
@stubs_bp.route('/financial', methods=['GET'])
@token_required
def get_financial(current_user):
    return jsonify([]), 200

# ---------- PEST ----------
@stubs_bp.route('/pest', methods=['GET'])
@token_required
def get_pest(current_user):
    return jsonify([]), 200

# ---------- DASHBOARD SUMMARY ----------
@stubs_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user):
    return jsonify({
        'active_valves': 0,
        'today_water_usage': 0,
        'temperature': 24.5,
        'soil_moisture': 45.0,
        'system_status': 'Operational'
    }), 200