from flask import Blueprint, request, jsonify
from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel
from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from sqlalchemy import func, desc
from collections import Counter
import re

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/tickets', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_ticket_analytics():
    """Obtener analítica de tickets"""
    try:
        # Contar tickets por estado
        tickets_abiertos = TicketModel.query.filter_by(status='abierto').count()
        tickets_en_progreso = TicketModel.query.filter_by(status='en_progreso').count()
        tickets_resueltos = TicketModel.query.filter_by(status='cerrado').count()
        
        # Contar tickets por prioridad
        tickets_urgentes = TicketModel.query.filter_by(priority='urgente').count()
        
        # Total de tickets
        total_tickets = TicketModel.query.count()
        
        return jsonify({
            'total_tickets': total_tickets,
            'tickets_abiertos': tickets_abiertos,
            'tickets_en_progreso': tickets_en_progreso,
            'tickets_resueltos': tickets_resueltos,
            'tickets_urgentes': tickets_urgentes
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/conversations', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_conversation_analytics():
    """Obtener analítica de conversaciones"""
    try:
        # Contar conversaciones
        total_conversaciones = ConversationModel.query.count()
        
        # Obtener temas más preguntados (preguntas de usuarios)
        user_messages = ChatMessageModel.query.filter_by(role='user').all()
        
        # Palabras clave comunes para identificar temas
        topic_keywords = {
            'productos': ['producto', 'productos', 'catalogo', 'catálogo', 'comprar', 'precio', 'disponible'],
            'pedidos': ['pedido', 'pedidos', 'orden', 'ordenes', 'comprar', 'carrito', 'checkout'],
            'envio': ['envío', 'envio', 'entrega', 'shipping', 'dirección', 'direccion'],
            'pagos': ['pago', 'pagos', 'tarjeta', 'efectivo', 'transferencia', 'dinero'],
            'devoluciones': ['devolución', 'devolucion', 'cambio', 'reembolso', 'cancelar'],
            'soporte': ['ayuda', 'soporte', 'problema', 'error', 'no funciona', 'ticket'],
            'cuenta': ['cuenta', 'usuario', 'perfil', 'registro', 'login', 'sesión'],
            'garantia': ['garantía', 'garantia', 'warranty', 'reparación', 'reparacion']
        }
        
        # Contar temas
        topic_counts = Counter()
        for message in user_messages:
            content_lower = message.content.lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in content_lower for keyword in keywords):
                    topic_counts[topic] += 1
        
        # Obtener los 5 temas más preguntados
        top_topics = topic_counts.most_common(5)
        
        # Obtener respuestas más frecuentes del chatbot
        assistant_messages = ChatMessageModel.query.filter_by(role='assistant').all()
        
        # Agrupar respuestas similares (simplificado)
        response_groups = {}
        for message in assistant_messages:
            content = message.content.strip()
            # Normalizar respuesta (primeras 50 caracteres para agrupar similares)
            key = content[:50].lower()
            if key not in response_groups:
                response_groups[key] = {
                    'content': content,
                    'count': 0
                }
            response_groups[key]['count'] += 1
        
        # Obtener las 5 respuestas más frecuentes
        top_responses = sorted(response_groups.values(), key=lambda x: x['count'], reverse=True)[:5]
        
        return jsonify({
            'total_conversaciones': total_conversaciones,
            'temas_mas_preguntados': [
                {'tema': topic, 'cantidad': count} for topic, count in top_topics
            ],
            'respuestas_mas_frecuentes': top_responses
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500




