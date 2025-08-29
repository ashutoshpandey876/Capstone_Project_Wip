from flask import Blueprint, request, jsonify
from models import User,db


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(username=username, password=password)  # store password as plain text (not recommended though)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
