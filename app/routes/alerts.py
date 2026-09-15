from flask import Blueprint, request, jsonify
from ..models.alert import Alert
from .. import db
from ..utils.auth import token_required
from ..services.alert_generator import generate_alerts
from ..socketio import socketio

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('', methods=['GET'])
@token_required
def get_alerts(current_user):
    query = Alert.query

    if request.args.get('unread') == 'true':
        query = query.filter_by(read=False)

    query = query.order_by(Alert.timestamp.desc())

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
    data = request.get_json()
    if not data.get('message'):
        return jsonify({'message': 'message is required'}), 400

    item = Alert(
        type=data.get('type', 'info'),
        message=data['message'],
    )
    db.session.add(item)
    db.session.commit()

    socketio.emit('alert:new', item.to_dict())
    socketio.emit('dashboard:refresh', {'reason': 'alert created'})

    return jsonify(item.to_dict()), 201


@alerts_bp.route('/<int:alert_id>', methods=['PUT'])
@token_required
def update_alert(current_user, alert_id):
    item = Alert.query.get(alert_id)
    if not item:
        return jsonify({'message': 'Alert not found'}), 404

    data = request.get_json()
    item.type = data.get('type', item.type)
    item.message = data.get('message', item.message)
    item.read = data.get('read', item.read)

    db.session.commit()

    socketio.emit('alert:updated', item.to_dict())
    socketio.emit('dashboard:refresh', {'reason': 'alert updated'})

    return jsonify(item.to_dict()), 200


@alerts_bp.route('/<int:alert_id>', methods=['DELETE'])
@token_required
def delete_alert(current_user, alert_id):
    item = Alert.query.get(alert_id)
    if not item:
        return jsonify({'message': 'Alert not found'}), 404
    db.session.delete(item)
    db.session.commit()

    socketio.emit('alert:deleted', {'id': alert_id})
    socketio.emit('dashboard:refresh', {'reason': 'alert deleted'})

    return jsonify({'message': 'Alert deleted'}), 200


@alerts_bp.route('/mark-all-read', methods=['POST'])
@token_required
def mark_all_read(current_user):
    count = Alert.query.filter_by(read=False).update({'read': True})
    db.session.commit()

    socketio.emit('alerts:all-read', {'count': count})
    socketio.emit('dashboard:refresh', {'reason': 'all alerts read'})

    return jsonify({'marked_read': count}), 200


@alerts_bp.route('/generate', methods=['POST'])
@token_required
def generate(current_user):
    result = generate_alerts()

    # ✅ If alerts were created, broadcast them
    for alert_data in result.get('alerts', []):
        socketio.emit('alert:new', alert_data)

    if result.get('created_count', 0) > 0:
        socketio.emit('dashboard:refresh', {'reason': 'alerts generated'})

    return jsonify(result), 200