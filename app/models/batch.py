from .. import db
from datetime import datetime

class Batch(db.Model):
    __tablename__ = 'batches'
    
    id = db.Column(db.Integer, primary_key=True)
    plot_id = db.Column(db.Integer, db.ForeignKey('plots.id'), nullable=False)
    crop_type = db.Column(db.String(50), nullable=False)
    variety = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    initial_count = db.Column(db.Integer, default=0)
    expected_yield = db.Column(db.Float, default=0)
    stage = db.Column(db.String(30), default='Sowing')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    care_logs = db.relationship('CareLog', backref='batch', lazy=True, cascade='all, delete-orphan')
    harvests = db.relationship('Harvest', backref='batch', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'plotId': self.plot_id,
            'cropType': self.crop_type,
            'variety': self.variety,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'initialCount': self.initial_count,
            'expectedYield': self.expected_yield,
            'stage': self.stage,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }