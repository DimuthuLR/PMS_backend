from flask_socketio import emit
from .socketio import socketio


@socketio.on('connect')
def handle_connect():
    print('🔌 Client connected')
    emit('server:hello', {'message': 'Connected to PMS realtime'})


@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')


@socketio.on('ping:server')
def handle_ping(data):
    print('📥 ping received:', data)
    emit('server:pong', {'received': data, 'ok': True})