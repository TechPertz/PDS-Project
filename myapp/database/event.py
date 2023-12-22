from myapp import db
from datetime import datetime

class EventData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('enrolled_device.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('event_label.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

class EventLabel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.String(50), nullable=False, unique=True)
    events = db.relationship('EventData', backref='event_label', lazy=True)
