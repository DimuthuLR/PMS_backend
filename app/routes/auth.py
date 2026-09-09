from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..utils.auth import hash_password, check_password, generate_token, token_required, admin_required

# ✅ This is the correct place to define the blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not check_password(password, user.password_hash):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = generate_token(user.id)
    return jsonify({'token': token, 'user': user.to_dict()}), 200

@auth_bp.route('/register', methods=['POST'])
@token_required
@admin_required
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'worker')
    if not username or not email or not password:
        return jsonify({'error': 'All fields required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    hashed = hash_password(password)
    new_user = User(username=username, email=email, password_hash=hashed, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@auth_bp.route('/me', methods=['GET'])
@token_required
def me():
    return jsonify(request.user.to_dict()), 200