from .. import db
from datetime import datetime

class Pest(db.Model):
    __tablename__ = 'pests'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    symptom = db.Column(db.String(200), nullable=False)
    severity = db.Column(db.Integer, default=3)
    date = db.Column(db.Date)
    image_url = db.Column(db.String(200))
    resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'batchId': self.batch_id,
            'symptom': self.symptom,
            'severity': self.severity,
            'date': self.date.isoformat() if self.date else None,
            'imageUrl': self.image_url,
            'resolved': self.resolved,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }