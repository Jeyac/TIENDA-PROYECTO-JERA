from flask import Blueprint, jsonify, request
from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.chatlog.application.conversation_service import ConversationService
from funcionalidades.core.infraestructura.database import db

conversation_bp = Blueprint('conversation', __name__)
conversation_service = ConversationService()


@conversation_bp.route('/conversations', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_user_conversations():
    """Obtener conversaciones del usuario autenticado"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        user_id = request.user_id
        conversations = conversation_service.get_user_conversations(user_id)
        return jsonify(conversations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@conversation_bp.route('/conversations/session', methods=['GET', 'OPTIONS'])
def get_session_conversations():
    """Obtener conversaciones de una sesión anónima"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({'error': 'Session ID requerido'}), 400
        
        conversations = conversation_service.get_session_conversations(session_id)
        return jsonify(conversations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@conversation_bp.route('/conversations', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_conversation():
    """Crear nueva conversación para usuario autenticado"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        user_id = request.user_id
        conversation = conversation_service.get_or_create_conversation(user_id=user_id)
        
        return jsonify({
            'id': conversation.id,
            'title': conversation.title,
            'created_at': conversation.created_at.isoformat(),
            'is_active': conversation.is_active
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@conversation_bp.route('/conversations/session', methods=['POST', 'OPTIONS'])
def create_session_conversation():
    """Crear nueva conversación para sesión anónima"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({'error': 'Session ID requerido'}), 400
        
        conversation = conversation_service.get_or_create_conversation(session_id=session_id)
        
        return jsonify({
            'id': conversation.id,
            'title': conversation.title,
            'created_at': conversation.created_at.isoformat(),
            'is_active': conversation.is_active
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@conversation_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_conversation_messages(conversation_id):
    """Obtener mensajes de una conversación"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        user_id = request.user_id
        limit = int(request.args.get('limit', 50))
        
        # Verificar que la conversación pertenece al usuario
        from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
        conversation = ConversationModel.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        messages = conversation_service.get_conversation_messages(conversation_id, limit)
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@conversation_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST', 'OPTIONS'])
@jwt_required()
def add_message(conversation_id):
    """Agregar mensaje a una conversación"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        data = request.get_json()
        if not data or 'content' not in data or 'role' not in data:
            return jsonify({'error': 'Contenido y rol requeridos'}), 400
        
        user_id = request.user_id
        
        # Verificar que la conversación pertenece al usuario
        from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
        conversation = ConversationModel.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        message = conversation_service.add_message(
            conversation_id=conversation_id,
            role=data['role'],
            content=data['content'],
            user_id=user_id
        )
        
        return jsonify({
            'id': message.id,
            'role': message.role,
            'content': message.content,
            'created_at': message.created_at.isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@conversation_bp.route('/conversations/<int:conversation_id>/close', methods=['POST', 'OPTIONS'])
@jwt_required()
def close_conversation(conversation_id):
    """Cerrar una conversación"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        user_id = request.user_id
        
        # Verificar que la conversación pertenece al usuario
        from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
        conversation = ConversationModel.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        success = conversation_service.close_conversation(conversation_id)
        if success:
            return jsonify({'message': 'Conversación cerrada correctamente'})
        else:
            return jsonify({'error': 'Error al cerrar conversación'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoints para sesiones anónimas (sin autenticación)
@conversation_bp.route('/conversations/session/<int:conversation_id>/messages', methods=['GET', 'OPTIONS'])
def get_session_conversation_messages(conversation_id):
    """Obtener mensajes de una conversación de sesión"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({'error': 'Session ID requerido'}), 400
        
        limit = int(request.args.get('limit', 50))
        
        # Verificar que la conversación pertenece a la sesión
        from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
        conversation = ConversationModel.query.filter_by(
            id=conversation_id,
            session_id=session_id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        messages = conversation_service.get_conversation_messages(conversation_id, limit)
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@conversation_bp.route('/conversations/session/<int:conversation_id>/messages', methods=['POST', 'OPTIONS'])
def add_session_message(conversation_id):
    """Agregar mensaje a una conversación de sesión"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        data = request.get_json()
        if not data or 'content' not in data or 'role' not in data:
            return jsonify({'error': 'Contenido y rol requeridos'}), 400
        
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({'error': 'Session ID requerido'}), 400
        
        # Verificar que la conversación pertenece a la sesión
        from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
        conversation = ConversationModel.query.filter_by(
            id=conversation_id,
            session_id=session_id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        message = conversation_service.add_message(
            conversation_id=conversation_id,
            role=data['role'],
            content=data['content'],
            user_id=None
        )
        
        return jsonify({
            'id': message.id,
            'role': message.role,
            'content': message.content,
            'created_at': message.created_at.isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500



