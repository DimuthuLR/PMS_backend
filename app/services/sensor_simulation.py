import random
import json
from datetime import datetime
from ..models.sensor import Sensor
from ..models.weather import Weather
from .. import db
from ..socketio import socketio  # ✅


def simulate_sensor_reading(previous=None):
    """Generate a new sensor reading (random walk from previous values)."""
    if previous:
        temp = previous.temperature + random.uniform(-0.5, 0.5)
        hum = previous.humidity + random.uniform(-1.5, 1.5)
        moisture = previous.soil_moisture + random.uniform(-2.0, 2.0)
    else:
        temp = random.uniform(20, 30)
        hum = random.uniform(45, 75)
        moisture = random.uniform(35, 60)

    temp = max(10, min(45, temp))
    hum = max(20, min(95, hum))
    moisture = max(10, min(90, moisture))

    return {
        'temperature': round(temp, 2),
        'humidity': round(hum, 2),
        'soil_moisture': round(moisture, 2),
    }


def get_or_create_sensor():
    sensor = Sensor.query.first()
    if not sensor:
        data = simulate_sensor_reading()
        sensor = Sensor(**data)
        db.session.add(sensor)
        db.session.commit()
    return sensor


def get_or_create_weather():
    weather = Weather.query.first()
    if not weather:
        weather = Weather(
            condition='Sunny',
            temp=27.0,
            wind_speed=6.0,
            humidity=60.0,
            forecast=generate_forecast(),
        )
        db.session.add(weather)
        db.session.commit()
    return weather


def generate_forecast(days=5):
    """Generate a 5-day mock forecast (returns JSON string)."""
    conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Stormy']
    forecast = []
    for i in range(days):
        forecast.append({
            'day': i + 1,
            'condition': random.choice(conditions),
            'high': round(random.uniform(24, 34), 1),
            'low': round(random.uniform(18, 24), 1),
            'rain_chance': random.randint(0, 100),
        })
    return json.dumps(forecast)


def emit_sensor_update(sensor):
    """Broadcast a sensor update to all connected clients."""
    socketio.emit('sensor:update', sensor.to_dict())


def emit_dashboard_refresh(reason='data changed'):
    """Nudge all dashboards to refetch."""
    socketio.emit('dashboard:refresh', {'reason': reason})