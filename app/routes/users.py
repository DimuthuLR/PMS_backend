from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..utils.auth import token_required, admin_required

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    """List all users (admin only)."""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
@admin_required
def get_user(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@users_bp.route('', methods=['POST'])
@token_required
@admin_required
def create_user(current_user):
    """Create a new user (admin only)."""
    data = request.get_json()

    if not data.get('username'):
        return jsonify({'message': 'username is required'}), 400
    if not data.get('email'):
        return jsonify({'message': 'email is required'}), 400
    if not data.get('password'):
        return jsonify({'message': 'password is required'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'user'),
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    # Check unique constraints before updating
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        user.username = data['username']

    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        user.email = data['email']

    if 'role' in data:
        user.role = data['role']

    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.to_dict()), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, user_id):
    # Prevent self-deletion
    if current_user.id == user_id:
        return jsonify({'message': 'You cannot delete your own account'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200