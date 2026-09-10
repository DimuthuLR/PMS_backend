from .. import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    assigned_to = db.Column(db.String(120))
    deadline = db.Column(db.Date)
    status = db.Column(db.String(30), default='pending')   # 'pending','in_progress','done'
    hours_logged = db.Column(db.Float, default=0.0)
    labor_cost = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'title': self.title,
            'assigned_to': self.assigned_to,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'status': self.status,
            'hours_logged': self.hours_logged,
            'labor_cost': self.labor_cost,
        }