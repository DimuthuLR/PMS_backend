from .. import db
from datetime import datetime

class Harvest(db.Model):
    __tablename__ = 'harvests'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    date = db.Column(db.Date)
    weight_kg = db.Column(db.Float, default=0)
    grade = db.Column(db.String(20), default='A')
    revenue = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'batchId': self.batch_id,
            'date': self.date.isoformat() if self.date else None,
            'weightKg': self.weight_kg,
            'grade': self.grade,
            'revenue': self.revenue,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }