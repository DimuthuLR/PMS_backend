from .. import db
from datetime import datetime

class CareLog(db.Model):
    __tablename__ = 'care_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    type = db.Column(db.String(20), default='organic')
    product = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50))
    method = db.Column(db.String(50))
    cost = db.Column(db.Float, default=0)
    date = db.Column(db.Date)
    next_due = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'batchId': self.batch_id,
            'type': self.type,
            'product': self.product,
            'quantity': self.quantity,
            'method': self.method,
            'cost': self.cost,
            'date': self.date.isoformat() if self.date else None,
            'nextDue': self.next_due.isoformat() if self.next_due else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }