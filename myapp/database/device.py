from myapp import db

class DeviceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    model_number = db.Column(db.String(50), nullable=False)
    enrolled_devices = db.relationship('EnrolledDevice', backref='device_model', lazy=True)

class EnrolledDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_location_id = db.Column(db.Integer, db.ForeignKey('service_location.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('device_model.id'), nullable=False)
    events = db.relationship('EventData', backref='enrolled_device', lazy=True)
