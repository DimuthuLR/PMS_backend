from .. import db
from datetime import datetime

class Actuator(db.Model):
    __tablename__ = 'actuators'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), default='valve')  # valve, pump
    zone = db.Column(db.String(50))
    status = db.Column(db.String(10), default='off')  # on, off
    mode = db.Column(db.String(10), default='manual') # manual, auto
    auto_threshold = db.Column(db.Integer, default=40) # for valves
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'zone': self.zone,
            'status': self.status,
            'mode': self.mode,
            'autoThreshold': self.auto_threshold,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }