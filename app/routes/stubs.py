from flask import Blueprint, jsonify
from ..utils.auth import token_required

stubs_bp = Blueprint('stubs', __name__)

# ---------- ALERTS (still a stub — will become real in Phase 6) ----------
@stubs_bp.route('/alerts', methods=['GET'])
@token_required
def get_alerts(current_user):
    return jsonify([]), 200


# ---------- DASHBOARD SUMMARY (still a stub — will become real in Phase 6) ----------
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