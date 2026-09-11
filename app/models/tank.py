from .. import db
from datetime import datetime

class Tank(db.Model):
    __tablename__ = 'tanks'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Float, default=0.0)                    # Liters
    capacity = db.Column(db.Float, default=1000.0)              # Liters
    pump_status = db.Column(db.String(10), default='off')       # 'on' or 'off'
    auto_mode = db.Column(db.Boolean, default=True)
    low_level_threshold = db.Column(db.Float, default=200.0)    # Below this, stop irrigation
    fill_level_threshold = db.Column(db.Float, default=900.0)   # Above this, stop filling
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'capacity': self.capacity,
            'pump_status': self.pump_status,
            'auto_mode': self.auto_mode,
            'low_level_threshold': self.low_level_threshold,
            'fill_level_threshold': self.fill_level_threshold,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }