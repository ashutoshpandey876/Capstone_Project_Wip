from datetime import datetime
from database import db

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    category_name = db.Column(db.String(50), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="active")  # active, cancelled, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
