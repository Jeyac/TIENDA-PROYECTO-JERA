from flask import request, current_app
from typing import Dict, List
import jwt

from funcionalidades.core.infraestructura.socketio import socketio
from funcionalidades.core.infraestructura.chat_gateway import ChatGateway
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.chatlog.application.conversation_service import ConversationService
from funcionalidades.core.infraestructura.database import db


# Inicializar gateway y servicios dentro del contexto de la aplicación
gateway = None
conversation_service = None
SESSIONS: Dict[str, List[dict]] = {}
# Almacenar información de usuario por sesión
USER_SESSIONS: Dict[str, int] = {}  # sid -> user_id

def get_gateway():
    """Obtener gateway inicializado dentro del contexto de la aplicación"""
    global gateway
    if gateway is None:
        from flask import current_app
        with current_app.app_context():
            gateway = ChatGateway()
    return gateway

def get_conversation_service():
    """Obtener servicio de conversación inicializado"""
    global conversation_service
    if conversation_service is None:
        conversation_service = ConversationService()
    return conversation_service


def get_user_id_from_token(auth_data=None):
    """Extraer user_id del token JWT si está disponible"""
    try:
        token = None
        
        # Intentar obtener el token del parámetro auth primero
        if auth_data and 'token' in auth_data:
            token = auth_data['token']
            print(f"Token obtenido desde auth parameter: {token[:20]}...")
        
        # Si no está en auth, intentar desde headers
        if not token:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                print(f"Token obtenido desde Authorization header: {token[:20]}...")
        
        if token:
            payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
            print(f"Token decodificado exitosamente para user_id: {payload.get('user_id')}")
            return payload.get('user_id')
        else:
            print(f"No se encontró token. Auth data: {auth_data}")
            print(f"Headers disponibles: {list(request.headers.keys())}")
    except Exception as e:
        print(f"Error extrayendo user_id del token: {e}")
        print(f"Auth data: {auth_data}")
    return None


@socketio.on('connect')
def on_connect(auth=None):
    sid = request.sid
    print(f"Intentando conectar socket con SID: {sid}")
    print(f"Auth parameter: {auth}")
    print(f"Headers de la petición: {dict(request.headers)}")
    
    user_id = get_user_id_from_token(auth)
    
    # Solo permitir conexión a usuarios autenticados
    if not user_id:
        print(f"Usuario no autenticado, rechazando conexión para SID: {sid}")
        socketio.emit('error', {'message': 'Debes iniciar sesión para usar el chat'}, room=sid)
        return False  # Rechazar la conexión
    
    # Verificar si es admin
    from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
    with current_app.app_context():
        user = UsuarioModel.query.get(user_id)
        if user and user.rol == 'administrador':
            print(f"⚠️  CHAT SOCKET: ADMIN CONECTÁNDOSE AL CHAT! Usuario: {user.username} (ID: {user_id})")
            print(f"⚠️  CHAT SOCKET: El admin no debería acceder al chat de soporte")
        else:
            print(f"✅ CHAT SOCKET: Usuario cliente conectándose: {user.username if user else 'Usuario'} (ID: {user_id})")
    
    print(f"Usuario autenticado con ID: {user_id}, aceptando conexión")
    SESSIONS[sid] = []
    USER_SESSIONS[sid] = user_id  # Almacenar user_id para esta sesión
    print(f"USER_SESSIONS actualizado: {USER_SESSIONS}")
    socketio.emit('server_message', {'message': 'Conectado al chat de soporte'}, room=sid)


@socketio.on('disconnect')
def on_disconnect():
    """Limpiar sesión cuando se desconecta"""
    sid = request.sid
    print(f"Usuario desconectado, limpiando sesión {sid}")
    
    # Limpiar datos de la sesión
    if sid in SESSIONS:
        del SESSIONS[sid]
    if sid in USER_SESSIONS:
        del USER_SESSIONS[sid]


@socketio.on('ask')
def on_ask(data):
    message = (data or {}).get('message', '')
    if not message:
        socketio.emit('answer', {'message': 'Mensaje vacío'})
        return
    
    # Obtener user_id de la sesión almacenada
    sid = request.sid
    print(f"Procesando mensaje para SID: {sid}")
    print(f"USER_SESSIONS actual: {USER_SESSIONS}")
    user_id = USER_SESSIONS.get(sid)
    if not user_id:
        print(f"Error: No se encontró user_id para la sesión {sid}")
        print(f"SID solicitado: {sid}")
        print(f"SIDs disponibles: {list(USER_SESSIONS.keys())}")
        socketio.emit('error', {'message': 'Sesión expirada. Por favor, recarga la página.'})
        return
    
    # Verificar si es admin enviando mensaje
    from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
    with current_app.app_context():
        user = UsuarioModel.query.get(user_id)
        if user and user.rol == 'administrador':
            print(f"⚠️  CHAT SOCKET: ADMIN ENVIANDO MENSAJE! Usuario: {user.username} (ID: {user_id})")
            print(f"⚠️  CHAT SOCKET: Mensaje: {message}")
        else:
            print(f"✅ CHAT SOCKET: Usuario cliente enviando mensaje: {user.username if user else 'Usuario'} (ID: {user_id})")
    
    print(f"Procesando mensaje de usuario {user_id}: {message}")
    
    # Asegurar contexto de aplicación para operaciones con SQLAlchemy
    with current_app.app_context():
        
        # Obtener o crear conversación activa
        conversation = get_conversation_service().get_or_create_conversation(user_id=user_id)
        
        # Obtener historial de la conversación
        history_messages = get_conversation_service().get_conversation_messages(conversation.id, limit=20)
        history = [{"role": msg['role'], "content": msg['content']} for msg in history_messages]
        
        # Agregar mensaje actual
        history.append({"role": "user", "content": message})
        
        # Guardar mensaje del usuario
        get_conversation_service().add_message(
            conversation_id=conversation.id,
            role='user',
            content=message,
            user_id=user_id
        )
        
        # Generar respuesta
        answer = get_gateway().answer(message, history=history)
        
        # Guardar respuesta del bot
        get_conversation_service().add_message(
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


