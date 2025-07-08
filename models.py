
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

STATUS_FOUND = "found"
STATUS_QUALIFIED = "qualified"
STATUS_CONVERTED = "converted"

class Prospect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact_info = db.Column(db.String(250))
    status = db.Column(db.String(20), default=STATUS_FOUND)
    qualifying_notes = db.Column(db.Text)
    conversion_notes = db.Column(db.Text)
    opportunity_size = db.Column(db.Float)
    success = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
