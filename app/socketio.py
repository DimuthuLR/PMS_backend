from flask_socketio import SocketIO

# Create the SocketIO instance — attach to app later in create_app()
# Using 'threading' mode: the recommended choice for new projects.
# No extra dependencies needed (no eventlet/gevent).
socketio = SocketIO(cors_allowed_origins='*', async_mode='threading')