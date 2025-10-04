from flask import request, current_app

from funcionalidades.core.infraestructura.socketio import socketio
from funcionalidades.core.infraestructura.chat_gateway import ChatGateway
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.core.infraestructura.database import db


gateway = ChatGateway()


@socketio.on('connect')
def on_connect():
    socketio.emit('server_message', {'message': 'Conectado al chat de soporte'})


@socketio.on('ask')
def on_ask(data):
    message = (data or {}).get('message', '')
    if not message:
        socketio.emit('answer', {'message': 'Mensaje vacío'})
        return
    # Asegurar contexto de aplicación para operaciones con SQLAlchemy
    with current_app.app_context():
        db.session.add(ChatMessageModel(user_id=None, role='user', content=message))
        db.session.commit()
        answer = gateway.answer(message)
        db.session.add(ChatMessageModel(user_id=None, role='assistant', content=answer))
        db.session.commit()
    socketio.emit('answer', {'message': answer})


