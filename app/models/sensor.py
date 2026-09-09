from .. import db
from datetime import datetime

class Sensor(db.Model):
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, default=0)
    humidity = db.Column(db.Float, default=0)
    soil_moisture = db.Column(db.Float, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'soilMoisture': self.soil_moisture,
            'lastUpdated': self.last_updated.isoformat() if self.last_updated else None
        }