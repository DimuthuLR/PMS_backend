from .. import db

class Harvest(db.Model):
    __tablename__ = 'harvests'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False, default=0.0)
    grade = db.Column(db.String(20), default='A')      # 'A', 'B', 'Rejects'
    revenue = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'date': self.date.isoformat() if self.date else None,
            'weight_kg': self.weight_kg,
            'grade': self.grade,
            'revenue': self.revenue,
        }