from .. import db
from datetime import datetime

class Financial(db.Model):
    __tablename__ = 'financials'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    cost_amount = db.Column(db.Float, default=0)
    date = db.Column(db.Date)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'batchId': self.batch_id,
            'category': self.category,
            'costAmount': self.cost_amount,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }