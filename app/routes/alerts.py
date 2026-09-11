from flask import Blueprint, request, jsonify
from ..models.alert import Alert
from .. import db
from ..utils.auth import token_required
from ..services.alert_generator import generate_alerts

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('', methods=['GET'])
@token_required
def get_alerts(current_user):
    """List alerts. Optional filters: ?unread=true, ?limit=20"""
    query = Alert.query

    unread_only = request.args.get('unread') == 'true'
    if unread_only:
        query = query.filter_by(read=False)

    # Newest first
    query = query.order_by(Alert.timestamp.desc())

    # Optional limit
    limit = request.args.get('limit', type=int)
    if limit:
        query = query.limit(limit)

    items = query.all()
    return jsonify([a.to_dict() for a in items]), 200


@alerts_bp.route('/<int:alert_id>', methods=['GET'])
@token_required
def get_alert(current_user, alert_id):
    item = Alert.query.get(alert_id)
    if not item:
        return jsonify({'message': 'Alert not found'}), 404
    return jsonify(item.to_dict()), 200


@alerts_bp.route('', methods=['POST'])
@token_required
def create_alert(current_user):
    """Manually create an alert."""
    data = request.get_json()
    if not data.get('message'):
        return jsonify({'message': 'message is required'}), 400

    item = Alert(
        type=data.get('type', 'info'),
        message=data['message'],
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@alerts_bp.route('/<int:alert_id>', methods=['PUT'])
@token_required
def update_alert(current_user, alert_id):
    """Update an alert (typically to mark it as read)."""
    item = Alert.query.get(alert_id)
    if not item:
        return jsonify({'message': 'Alert not found'}), 404

    data = request.get_json()
    item.type = data.get('type', item.type)
    item.message = data.get('message', item.message)
    item.read = data.get('read', item.read)

    db.session.commit()
    return jsonify(item.to_dict()), 200


@alerts_bp.route('/<int:alert_id>', methods=['DELETE'])
@token_required
def delete_alert(current_user, alert_id):
    item = Alert.query.get(alert_id)
    if not item:
        return jsonify({'message': 'Alert not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Alert deleted'}), 200


@alerts_bp.route('/mark-all-read', methods=['POST'])
@token_required
def mark_all_read(current_user):
    """Mark every unread alert as read."""
    count = Alert.query.filter_by(read=False).update({'read': True})
    db.session.commit()
    return jsonify({'marked_read': count}), 200


@alerts_bp.route('/generate', methods=['POST'])
@token_required
def generate(current_user):
    """Analyze current system state and create alerts for anomalies."""
    result = generate_alerts()
    return jsonify(result), 200