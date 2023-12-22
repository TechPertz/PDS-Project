from myapp import db
from sqlalchemy import DateTime

class EnergyPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(10), db.ForeignKey('address.zip_code'), nullable=False)
    hour = db.Column(DateTime, nullable=False)
    rate = db.Column(db.Float, nullable=False)
