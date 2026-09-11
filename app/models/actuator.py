from .. import db
from datetime import datetime

class Actuator(db.Model):
    __tablename__ = 'actuators'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(30), default='valve')       # 'valve' or 'pump'
    zone = db.Column(db.String(60))                        # e.g., "Zone A"
    status = db.Column(db.String(10), default='off')       # 'on' or 'off'
    mode = db.Column(db.String(10), default='manual')      # 'manual' or 'auto'
    auto_threshold = db.Column(db.Float, default=30.0)     # Soil moisture % below which to activate
    last_toggled = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'zone': self.zone,
            'status': self.status,
            'mode': self.mode,
            'auto_threshold': self.auto_threshold,
            'last_toggled': self.last_toggled.isoformat() if self.last_toggled else None,
        }