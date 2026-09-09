from .. import db
from datetime import datetime

class Tank(db.Model):
    __tablename__ = 'tank'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Float, default=0)
    capacity = db.Column(db.Float, default=1000)
    pump_status = db.Column(db.String(10), default='off')
    auto_mode = db.Column(db.Boolean, default=True)
    low_level_threshold = db.Column(db.Float, default=20)
    fill_level_threshold = db.Column(db.Float, default=80)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'capacity': self.capacity,
            'pumpStatus': self.pump_status,
            'autoMode': self.auto_mode,
            'lowLevelThreshold': self.low_level_threshold,
            'fillLevelThreshold': self.fill_level_threshold,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }