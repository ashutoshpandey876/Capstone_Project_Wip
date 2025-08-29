from flask import Blueprint, request, jsonify
from models import Reservation
from database import db
import requests
from datetime import datetime

reservation_routes = Blueprint('reservation_routes', __name__)

ROOM_SERVICE_URL = 'http://room_service:5000'  # Change accordingly

def call_room_service_available(category, from_date, to_date):
    params = {
        'category': category,
        'from_date': from_date,
        'to_date': to_date
    }
    resp = requests.get(f"{ROOM_SERVICE_URL}/rooms/available", params=params)
    if resp.status_code != 200:
        raise Exception("Room service not available")
    return resp.json()

def call_room_service_update_booking(room_number, category_name, from_date, to_date, action="book"):
    """
    action: "book" or "release"
    """
    data = {
        "room_number": room_number,
        "category_name": category_name,
        "from_date": from_date,
        "to_date": to_date,
        "action": action
    }
    resp = requests.post(f"{ROOM_SERVICE_URL}/rooms/update_booking", json=data)
    if resp.status_code != 200:
        raise Exception(f"Failed to {action} room booking in room service")
    return resp.json()

@reservation_routes.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    print('Incoming data:', data) 
    category = data.get('category')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    user_id = data.get('user_id')

    if not all([category, check_in, check_out, user_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Check available rooms in room service
        available_rooms = call_room_service_available(category, check_in, check_out)
        if not available_rooms:
            return jsonify({"error": "No available rooms for these dates"}), 404

        room_to_book = available_rooms[0]['number']

        # Call room service to book (update unavailable_dates)
        call_room_service_update_booking(room_to_book, category, check_in, check_out, action="book")

        # Save reservation locally
        reservation = Reservation(
            user_id=user_id,
            room_number=room_to_book,
            category_name=category,
            check_in=datetime.strptime(check_in, '%Y-%m-%d').date(),
            check_out=datetime.strptime(check_out, '%Y-%m-%d').date(),
            status="active"
        )
        db.session.add(reservation)
        db.session.commit()

        return jsonify({
            "message": "Reservation created successfully",
            "reservation_id": reservation.id,
            "room_number": room_to_book,
            "category":category
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservation_routes.route('/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    data = request.json
    new_category = data.get('category')
    new_check_in = data.get('check_in')
    new_check_out = data.get('check_out')

    reservation = Reservation.query.get(reservation_id)
    if not reservation or reservation.status != "active":
        return jsonify({"error": "Reservation not found or not active"}), 404

    old_room_number = reservation.room_number
    old_category = reservation.category_name
    old_check_in = reservation.check_in.strftime('%Y-%m-%d')
    old_check_out = reservation.check_out.strftime('%Y-%m-%d')

    try:
        # Release old booking dates in room service
        call_room_service_update_booking(old_room_number, old_category, old_check_in, old_check_out, action="release")

        # Determine new values (if not provided keep old)
        category = new_category if new_category else reservation.category_name
        check_in = new_check_in if new_check_in else old_check_in
        check_out = new_check_out if new_check_out else old_check_out

        # Check available rooms for new params
        available_rooms = call_room_service_available(category, check_in, check_out)
        if not available_rooms:
            # Re-book old booking back because new dates/category not available
            call_room_service_update_booking(old_room_number, old_category, old_check_in, old_check_out, action="book")
            return jsonify({"error": "No available rooms for the updated dates or category"}), 400

        # Book new room (pick first available)
        new_room = available_rooms[0]['number']
        call_room_service_update_booking(new_room, category, check_in, check_out, action="book")

        # Update reservation details
        reservation.room_number = new_room
        reservation.category_name = category
        reservation.check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
        reservation.check_out = datetime.strptime(check_out, '%Y-%m-%d').date()
        db.session.commit()

        return jsonify({"message": "Reservation updated", "reservation_id": reservation.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservation_routes.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation or reservation.status != "active":
        return jsonify({"error": "Reservation not found or already cancelled"}), 404

    try:
        # Release booking in room service
        call_room_service_update_booking(
            reservation.room_number,
            reservation.category_name,
            reservation.check_in.strftime('%Y-%m-%d'),
            reservation.check_out.strftime('%Y-%m-%d'),
            action="release"
        )

        reservation.status = "cancelled"
        db.session.commit()

        return jsonify({"message": "Reservation cancelled successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservation_routes.route('/reservations', methods=['GET'])
def list_reservations():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id query param required"}), 400

    reservations = Reservation.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "reservation_id": r.id,
        "room_number": r.room_number,
        "category": r.category_name,
        "check_in": r.check_in.strftime('%Y-%m-%d'),
        "check_out": r.check_out.strftime('%Y-%m-%d'),
        "status": r.status
    } for r in reservations])
