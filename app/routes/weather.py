from flask import Blueprint, request, jsonify
from ..models.weather import Weather
from .. import db
from ..utils.auth import token_required
from ..services.sensor_simulation import get_or_create_weather, generate_forecast
from datetime import datetime

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('', methods=['GET'])
@token_required
def get_weather(current_user):
    weather = get_or_create_weather()
    return jsonify(weather.to_dict()), 200

@weather_bp.route('', methods=['PUT'])
@token_required
def update_weather(current_user):
    weather = get_or_create_weather()
    data = request.get_json()
    weather.condition = data.get('condition', weather.condition)
    weather.temp = data.get('temp', weather.temp)
    weather.wind_speed = data.get('wind_speed', weather.wind_speed)
    weather.humidity = data.get('humidity', weather.humidity)
    if 'forecast' in data:
        import json
        weather.forecast = json.dumps(data['forecast'])
    weather.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify(weather.to_dict()), 200

@weather_bp.route('/refresh', methods=['POST'])
@token_required
def refresh_weather(current_user):
    """Refresh weather data with new mock values (dev-friendly)."""
    weather = get_or_create_weather()
    weather.forecast = generate_forecast()
    weather.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify(weather.to_dict()), 200