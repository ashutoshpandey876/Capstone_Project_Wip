from database import db
from sqlalchemy.types import JSON
from sqlalchemy.ext.mutable import MutableList

class RoomCategory(db.Model):
    __tablename__ = 'room_categories'

    name = db.Column(db.String(50), primary_key=True)  # e.g., "Deluxe"
    pricePerNight = db.Column(db.Float, nullable=False)
    image_urls = db.Column(JSON)
    description = db.Column(JSON)
    amenities = db.Column(JSON)

    rooms = db.relationship('Room', backref='category', lazy=True)

class Room(db.Model):
    __tablename__ = 'rooms'

    number = db.Column(db.String(10), primary_key=True)  # e.g., "101"
    
    category_name = db.Column(
        db.String(50),
        db.ForeignKey('room_categories.name'),
        nullable=False
    )


    unavailable_dates = db.Column(
        MutableList.as_mutable(JSON),
        default=list
    )
