from flask_socketio import emit, join_room
from .socketio import socketio


@socketio.on('connect')
def handle_connect():
    """Called when a client opens a WebSocket connection."""
    print('🔌 Client connected')
    emit('server:hello', {'message': 'Connected to PMS realtime'})


@socketio.on('disconnect')
def handle_disconnect():
    """Called when a client disconnects."""
    print('❌ Client disconnected')


@socketio.on('ping:server')
def handle_ping(data):
    """Simple echo to test connectivity."""
    emit('server:pong', {'received': data, 'ok': True})