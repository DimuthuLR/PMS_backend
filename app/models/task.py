from .. import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.String(80))
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    hours_logged = db.Column(db.Float, default=0)
    labor_cost = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'batchId': self.batch_id,
            'title': self.title,
            'assignedTo': self.assigned_to,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'status': self.status,
            'hoursLogged': self.hours_logged,
            'laborCost': self.labor_cost,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }