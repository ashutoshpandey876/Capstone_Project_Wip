from flask import Blueprint, jsonify,request
from datetime import datetime, date

from models import Room,RoomCategory
from database import db

room_routes = Blueprint('room_routes', __name__)

@room_routes.route('/rooms', methods=['GET'])
def get_all_rooms():
    rooms = Room.query.all()
    return jsonify([{
        'number': room.number,
        'category': room.category_name,
        'unavailable_dates':room.unavailable_dates
    } for room in rooms])



@room_routes.route('/rooms/available', methods=['GET'])
def check_room_availability():
    category = request.args.get('category')
    from_date_str = request.args.get('from_date')
    to_date_str = request.args.get('to_date')

    if not all([category, from_date_str, to_date_str]):
        return jsonify({'error': 'Missing parameters: category, from_date, to_date'}), 400

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Get all rooms in the category except those under maintenance
    rooms = Room.query.filter_by(category_name=category).all()

    available_rooms = []

    def dates_overlap(start1, end1, start2, end2):
         return not (end1 <= start2 or end2 <= start1)

    for room in rooms:
        # If none of the unavailable dates overlap with requested dates
        if all(
            not dates_overlap(
                from_date,
                to_date,
                datetime.strptime(slot['from'], '%Y-%m-%d').date(),
                datetime.strptime(slot['to'], '%Y-%m-%d').date()
            ) for slot in room.unavailable_dates
        ):
            available_rooms.append({
                'number': room.number,
                'category': room.category_name,
                'unavailable_dates': room.unavailable_dates
            })

    return jsonify(available_rooms)

@room_routes.route('/rooms/update_booking', methods=['POST'])
def update_booking():
    data = request.json
    room_number = data.get('room_number')
    category_name = data.get('category_name')
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    action = data.get('action')  # "book" or "release"

    room = Room.query.filter_by(number=room_number, category_name=category_name).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    # Manage unavailable_dates list
    if action == "book":
        # Add date range if not exists
        room.unavailable_dates.append({"from": from_date, "to": to_date})
    elif action == "release":
        # Remove matching date range(s)
        room.unavailable_dates = [
            d for d in room.unavailable_dates if not (d['from'] == from_date and d['to'] == to_date)
        ]
    else:
        return jsonify({"error": "Invalid action"}), 400

    db.session.commit()
    return jsonify({"message": f"Room {action}ed successfully"})



@room_routes.route('/room-categories/available', methods=['GET'])
def get_available_categories():
    from_date_str = request.args.get('from_date')
    to_date_str = request.args.get('to_date')
    if not from_date_str or not to_date_str:
        return jsonify({"error": "Missing parameters: from_date, to_date"}), 400

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format; use YYYY-MM-DD"}), 400

    available_categories = []
    for category in RoomCategory.query.all():
        for room in category.rooms:
            # check room availability
            overlaps = False
            for slot in room.unavailable_dates or []:
                booked_from = datetime.strptime(slot['from'], '%Y-%m-%d').date()
                booked_to = datetime.strptime(slot['to'], '%Y-%m-%d').date()
                # check overlap (treat checkout as free)
                if not (to_date <= booked_from or booked_to <= from_date):
                    overlaps = True
                    break
            if not overlaps:
                available_categories.append({
                    'name': category.name,
                    'pricePerNight': category.pricePerNight,
                    'image_urls': category.image_urls,
                    'description': category.description,
                    'amenities': category.amenities
                })
                break  # no need to check more rooms in this category

    return jsonify(available_categories), 200

