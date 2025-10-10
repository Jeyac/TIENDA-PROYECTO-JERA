from flask import request, current_app
from typing import Dict, List
import jwt

from funcionalidades.core.infraestructura.socketio import socketio
from funcionalidades.core.infraestructura.chat_gateway import ChatGateway
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.chatlog.application.conversation_service import ConversationService
from funcionalidades.core.infraestructura.database import db


gateway = ChatGateway()
conversation_service = ConversationService()
SESSIONS: Dict[str, List[dict]] = {}


def get_user_id_from_token():
    """Extraer user_id del token JWT si está disponible"""
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
            return payload.get('user_id')
    except Exception as e:
        print(f"Error extrayendo user_id del token: {e}")
    return None


@socketio.on('connect')
def on_connect(auth=None):
    sid = request.sid
    user_id = get_user_id_from_token()
    
    # Solo permitir conexión a usuarios autenticados
    if not user_id:
        socketio.emit('error', {'message': 'Debes iniciar sesión para usar el chat'}, room=sid)
        return False  # Rechazar la conexión
    
    SESSIONS[sid] = []
    socketio.emit('server_message', {'message': 'Conectado al chat de soporte'}, room=sid)


@socketio.on('ask')
def on_ask(data):
    message = (data or {}).get('message', '')
    if not message:
        socketio.emit('answer', {'message': 'Mensaje vacío'})
        return
    
    # Verificar autenticación antes de procesar
    user_id = get_user_id_from_token()
    if not user_id:
        socketio.emit('error', {'message': 'Sesión expirada. Por favor, recarga la página.'})
        return
    
    # Asegurar contexto de aplicación para operaciones con SQLAlchemy
    with current_app.app_context():
        sid = request.sid
        
        # Obtener o crear conversación activa
        conversation = conversation_service.get_or_create_conversation(user_id=user_id)
        
        # Obtener historial de la conversación
        history_messages = conversation_service.get_conversation_messages(conversation.id, limit=20)
        history = [{"role": msg['role'], "content": msg['content']} for msg in history_messages]
        
        # Agregar mensaje actual
        history.append({"role": "user", "content": message})
        
        # Guardar mensaje del usuario
        conversation_service.add_message(
            conversation_id=conversation.id,
            role='user',
            content=message,
            user_id=user_id
        )
        
        # Generar respuesta
        answer = gateway.answer(message, history=history)
        
        # Guardar respuesta del bot
        conversation_service.add_message(
            conversation_id=conversation.id,
            role='assistant',
            content=answer,
            user_id=user_id
        )
        
        # El resumen se maneja automáticamente en el ConversationService
        # cuando se alcanzan 10 mensajes
        
        # Detectar si el usuario necesita crear un ticket
        ticket_keywords = ['problema', 'error', 'no funciona', 'ayuda', 'soporte', 'ticket', 'queja', 'reclamo']
        needs_ticket = any(keyword in message.lower() for keyword in ticket_keywords)
        
        response_data = {'message': answer}
        
        # Si parece que necesita un ticket, sugerir crear uno
        if needs_ticket and conversation.message_count > 3:  # Después de algunos mensajes
            response_data['suggest_ticket'] = True
            response_data['ticket_message'] = 'Parece que tienes un problema que requiere seguimiento. ¿Te gustaría crear un ticket de soporte para que nuestro equipo pueda ayudarte mejor?'
        
    socketio.emit('answer', response_data)


@socketio.on('create_ticket')
def on_create_ticket(data):
    """Crear ticket desde el chat"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            socketio.emit('error', {'message': 'Sesión expirada. Por favor, recarga la página.'})
            return
        
        conversation_id = data.get('conversation_id')
        title = data.get('title', 'Ticket desde chat')
        description = data.get('description', '')
        priority = data.get('priority', 'media')
        category = data.get('category', 'soporte')
        
        if not conversation_id:
            socketio.emit('error', {'message': 'ID de conversación requerido'})
            return
        
        with current_app.app_context():
            from funcionalidades.tickets.application.ticket_service import TicketService
            ticket_service = TicketService()
            
            ticket = ticket_service.create_ticket_from_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                category=category
            )
            
            socketio.emit('ticket_created', {
                'ticket_id': ticket.id,
                'title': ticket.title,
                'status': ticket.status,
                'message': 'Ticket creado exitosamente. Nuestro equipo se pondrá en contacto contigo pronto.'
            })
            
    except Exception as e:
        socketio.emit('error', {'message': f'Error creando ticket: {str(e)}'})


