from .. import db
from datetime import datetime

class CareLog(db.Model):
    __tablename__ = 'care_logs'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    type = db.Column(db.String(30), nullable=False)     # 'organic' or 'chemical'
    product = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.String(60))                 # e.g., "50ml", "2kg"
    method = db.Column(db.String(60))                   # e.g., "spray", "drench"
    cost = db.Column(db.Float, default=0.0)
    date = db.Column(db.Date, nullable=False)
    next_due = db.Column(db.Date)                       # PHI / next scheduled application

    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'type': self.type,
            'product': self.product,
            'quantity': self.quantity,
            'method': self.method,
            'cost': self.cost,
            'date': self.date.isoformat() if self.date else None,
            'next_due': self.next_due.isoformat() if self.next_due else None,
        }