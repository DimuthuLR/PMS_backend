from .. import db
from datetime import datetime
import json

class Weather(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(50), default='Sunny')
    temp = db.Column(db.Float, default=27.0)
    wind_speed = db.Column(db.Float, default=5.0)
    humidity = db.Column(db.Float, default=55.0)
    forecast = db.Column(db.Text)  # Stored as JSON string
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        forecast_list = []
        if self.forecast:
            try:
                forecast_list = json.loads(self.forecast)
            except (ValueError, TypeError):
                forecast_list = []
        return {
            'id': self.id,
            'condition': self.condition,
            'temp': self.temp,
            'wind_speed': self.wind_speed,
            'humidity': self.humidity,
            'forecast': forecast_list,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }