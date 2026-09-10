from .. import db
from datetime import datetime

class Batch(db.Model):
    __tablename__ = 'batches'

    id = db.Column(db.Integer, primary_key=True)
    plot_id = db.Column(db.Integer, db.ForeignKey('plots.id'), nullable=False)
    crop_type = db.Column(db.String(80), nullable=False)     # e.g., "Chili"
    variety = db.Column(db.String(80))                        # e.g., "Bird's Eye"
    start_date = db.Column(db.Date, nullable=False)
    initial_count = db.Column(db.Integer, default=0)          # Number of seedlings planted
    expected_yield = db.Column(db.Float, default=0.0)         # Expected kg
    stage = db.Column(db.String(50), default='Sowing')        # Lifecycle stage
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'plot_id': self.plot_id,
            'plot_name': self.plot.name if self.plot else None,
            'crop_type': self.crop_type,
            'variety': self.variety,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'initial_count': self.initial_count,
            'expected_yield': self.expected_yield,
            'stage': self.stage,
            'notes': self.notes
        }