from .. import db

class Pest(db.Model):
    __tablename__ = 'pests'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    symptom = db.Column(db.String(200), nullable=False)
    severity = db.Column(db.Integer, default=1)          # 1 to 5
    date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String(300))
    resolved = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'symptom': self.symptom,
            'severity': self.severity,
            'date': self.date.isoformat() if self.date else None,
            'image_url': self.image_url,
            'resolved': self.resolved,
        }