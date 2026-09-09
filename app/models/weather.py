from .. import db
from datetime import datetime

class Weather(db.Model):
    __tablename__ = 'weather'
    
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(50))
    temp = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    humidity = db.Column(db.Float)
    forecast = db.Column(db.JSON)  # store list of days
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'condition': self.condition,
            'temp': self.temp,
            'windSpeed': self.wind_speed,
            'humidity': self.humidity,
            'forecast': self.forecast,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }