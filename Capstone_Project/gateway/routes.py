import requests
from flask import Blueprint, request, jsonify


gateway_routes = Blueprint('gateway_routes', __name__)

ROOM_SERVICE_URL = 'http://room_service:5000'
RESERVATION_SERVICE_URL = 'http://reservation_service:5001'
AUTH_SERVICE_URL = 'http://auth_service:5003'  # Adjust if your auth service runs on a different port



@gateway_routes.route('/api/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        response = requests.post(f"{AUTH_SERVICE_URL}/auth/register", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Auth service is unavailable", "details": str(e)}), 503

@gateway_routes.route('/api/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        response = requests.post(f"{AUTH_SERVICE_URL}/auth/login", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Auth service is unavailable", "details": str(e)}), 503

# 1. Get available rooms
@gateway_routes.route('/api/rooms/available', methods=['GET'])
def get_available_rooms():
    category = request.args.get('category')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    params = {
        'category': category,
        'from_date': from_date,
        'to_date': to_date
    }

    # Forward GET request to Room Service
    try:
        response = requests.get(f"{ROOM_SERVICE_URL}/rooms/available", params=params)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Room service is unavailable", "details": str(e)}), 503

# 2. Create reservation
@gateway_routes.route('/api/reservations', methods=['POST'])
def create_reservation():
    data = request.json

    # Forward POST request to Reservation Service
    try:
        response = requests.post(f"{RESERVATION_SERVICE_URL}/reservations", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Reservation service is unavailable", "details": str(e)}), 503

# 3. Get reservations by user_id
@gateway_routes.route('/api/reservations', methods=['GET'])
def get_user_reservations():
     user_id = request.args.get('user_id')
     if not user_id:
        return jsonify({"error": "Missing user_id query parameter"}), 400

     params = {'user_id': user_id}

    # Forward GET request to Reservation Service
     try:
        response = requests.get(f"{RESERVATION_SERVICE_URL}/reservations", params=params)
        return jsonify(response.json()), response.status_code
     except requests.exceptions.RequestException as e:
        return jsonify({"error": "Reservation service is unavailable", "details": str(e)}), 503

# 4. Update reservation
@gateway_routes.route('/api/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    data = request.json

    # Forward PUT request to Reservation Service
    try:
        response = requests.put(f"{RESERVATION_SERVICE_URL}/reservations/{reservation_id}", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Reservation service is unavailable", "details": str(e)}), 503

# 5. Delete reservation
@gateway_routes.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    try:
        response = requests.delete(f"{RESERVATION_SERVICE_URL}/reservations/{reservation_id}")
        if response.status_code == 204:
            return '', 204
        else:
            return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Reservation service is unavailable", "details": str(e)}), 503
    
    # Fetch available categories by date
@gateway_routes.route('/api/room-categories/available', methods=['GET'])
def gateway_get_available_categories():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    if not from_date or not to_date:
        return jsonify({"error": "Missing parameters: from_date, to_date"}), 400

    params = {'from_date': from_date, 'to_date': to_date}
    try:
        resp = requests.get(f"{ROOM_SERVICE_URL}/room-categories/available", params=params)
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Room service unavailable", "details": str(e)}), 503

