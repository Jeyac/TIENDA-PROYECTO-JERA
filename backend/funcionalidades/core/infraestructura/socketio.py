from flask_socketio import SocketIO


socketio = SocketIO(
    cors_allowed_origins=['http://localhost:3000'],
    logger=False,
    engineio_logger=False
)

__all__ = ["socketio"]


