from flask_socketio import SocketIO


socketio = SocketIO(
    cors_allowed_origins=['http://localhost:3000'],
    logger=True,
    engineio_logger=True
)

__all__ = ["socketio"]


