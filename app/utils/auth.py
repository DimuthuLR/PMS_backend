import jwt
from functools import wraps
from flask import request, jsonify, current_app
from ..models.user import User

def create_token(user):
    """Generates a JWT token for a given user"""
    payload = {
        'user_id': user.id,
        'role': user.role
    }
    # Encode the payload with the secret key
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def token_required(f):
    """Decorator to protect routes - checks for a valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            # Fetch the user from the database
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Pass the current user to the route function
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to restrict access to admin users only"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Admin privileges required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def manager_required(f):
    """Decorator to restrict access to admin or manager users only"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role not in ['admin', 'manager']:
            return jsonify({'message': 'Manager or Admin privileges required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated