from flask import Blueprint, request, jsonify
from ..models import Weather
from .. import db
from ..utils.auth import token_required
from ..services.weather_service import WeatherService
from datetime import datetime

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('', methods=['GET'])
@token_required
def get_weather():
    """Get weather data (fetches from API if stale)"""
    weather = Weather.query.first()
    
    # Check if we need to refresh (data older than 1 hour)
    refresh = False
    if weather and weather.updated_at:
        age = (datetime.utcnow() - weather.updated_at).total_seconds()
        if age > 3600:  # 1 hour
            refresh = True
    
    if not weather or refresh:
        # Fetch fresh data from OpenWeatherMap
        current = WeatherService.get_current_weather()
        forecast = WeatherService.get_forecast()
        
        if not weather:
            weather = Weather()
            db.session.add(weather)
        
        weather.condition = current['condition']
        weather.temp = current['temp']
        weather.wind_speed = current['wind_speed']
        weather.humidity = current['humidity']
        weather.forecast = forecast
        weather.updated_at = datetime.utcnow()
        db.session.commit()
    
    return jsonify(weather.to_dict()), 200

@weather_bp.route('', methods=['PUT'])
@token_required
def update_weather():
    """Manually update weather (e.g., for testing)"""
    weather = Weather.query.first()
    if not weather:
        weather = Weather()
        db.session.add(weather)
    
    data = request.get_json()
    weather.condition = data.get('condition', weather.condition)
    weather.temp = data.get('temp', weather.temp)
    weather.wind_speed = data.get('windSpeed', weather.wind_speed)
    weather.humidity = data.get('humidity', weather.humidity)
    weather.forecast = data.get('forecast', weather.forecast)
    weather.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(weather.to_dict()), 200

@weather_bp.route('/refresh', methods=['POST'])
@token_required
def refresh_weather():
    """Force refresh weather from API"""
    current = WeatherService.get_current_weather()
    forecast = WeatherService.get_forecast()
    
    weather = Weather.query.first()
    if not weather:
        weather = Weather()
        db.session.add(weather)
    
    weather.condition = current['condition']
    weather.temp = current['temp']
    weather.wind_speed = current['wind_speed']
    weather.humidity = current['humidity']
    weather.forecast = forecast
    weather.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(weather.to_dict()), 200