from .. import db
from datetime import datetime

class Plot(db.Model):
    __tablename__ = 'plots'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grid_ref = db.Column(db.String(20))
    dimensions = db.Column(db.String(50))
    soil_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    batches = db.relationship('Batch', backref='plot', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gridRef': self.grid_ref,
            'dimensions': self.dimensions,
            'soilType': self.soil_type,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }