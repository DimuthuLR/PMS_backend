from .. import db

class Financial(db.Model):
    __tablename__ = 'financials'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    category = db.Column(db.String(60), nullable=False)   # e.g., 'seeds','fertilizer','labor','water'
    cost_amount = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'category': self.category,
            'cost_amount': self.cost_amount,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
        }