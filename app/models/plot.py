from .. import db
from datetime import datetime

class Plot(db.Model):
    __tablename__ = 'plots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    grid_ref = db.Column(db.String(50))          # e.g., "A1", "Greenhouse-3"
    dimensions = db.Column(db.String(50))         # e.g., "10m x 5m"
    soil_type = db.Column(db.String(80))          # e.g., "Loamy", "Sandy"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: One plot can have many batches
    batches = db.relationship('Batch', backref='plot', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'grid_ref': self.grid_ref,
            'dimensions': self.dimensions,
            'soil_type': self.soil_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'batch_count': len(self.batches)   # Helpful for the frontend
        }