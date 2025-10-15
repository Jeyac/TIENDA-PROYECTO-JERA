from flask import Blueprint, request, jsonify
from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.analytics.application.use_cases.obtener_analytics_conversaciones_use_case import ObtenerAnalyticsConversacionesUseCase
from funcionalidades.analytics.application.use_cases.obtener_analytics_tickets_use_case import ObtenerAnalyticsTicketsUseCase
from funcionalidades.analytics.application.use_cases.obtener_analytics_mensajes_use_case import ObtenerAnalyticsMensajesUseCase
from funcionalidades.analytics.application.use_cases.obtener_analytics_combinados_use_case import ObtenerAnalyticsCombinadosUseCase
from funcionalidades.analytics.infrastructure.analytics_repository_impl import AnalyticsRepositoryImpl

analytics_bp = Blueprint('analytics', __name__)

# Inicializar casos de uso
analytics_repository = AnalyticsRepositoryImpl()
obtener_analytics_conversaciones_use_case = ObtenerAnalyticsConversacionesUseCase(analytics_repository)
obtener_analytics_tickets_use_case = ObtenerAnalyticsTicketsUseCase(analytics_repository)
obtener_analytics_mensajes_use_case = ObtenerAnalyticsMensajesUseCase(analytics_repository)
obtener_analytics_combinados_use_case = ObtenerAnalyticsCombinadosUseCase(analytics_repository)

@analytics_bp.route('/tickets', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_ticket_analytics():
    """Obtener analítica de tickets"""
    try:
        days = int(request.args.get('days', 30))
        analytics = obtener_analytics_tickets_use_case.ejecutar(days)
        
        return jsonify({
            'total_tickets': analytics.total_tickets,
            'tickets_abiertos': analytics.open_tickets,
            'tickets_en_progreso': analytics.tickets_by_status.get('en_progreso', 0),
            'tickets_cerrados': analytics.closed_tickets,
            'tickets_resueltos': analytics.resolved_tickets,
            'tickets_urgentes': analytics.tickets_by_priority.get('urgente', 0),
            'tickets_por_prioridad': analytics.tickets_by_priority,
            'tickets_por_categoria': analytics.tickets_by_category,
            'tickets_por_estado': analytics.tickets_by_status,
            'tiempo_promedio_resolucion': analytics.avg_resolution_time,
            'tickets_por_dia': analytics.tickets_by_day,
            'periodo_dias': days
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/conversations', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_conversation_analytics():
    """Obtener analítica de conversaciones"""
    try:
        days = int(request.args.get('days', 30))
        print(f"🔍 ANALYTICS: Solicitando analytics de conversaciones para {days} días")
        
        analytics = obtener_analytics_conversaciones_use_case.ejecutar(days)
        
        print(f"📊 ANALYTICS: Datos generados:")
        print(f"  - Total conversaciones: {analytics.total_conversations}")
        print(f"  - Total mensajes: {analytics.total_messages}")
        print(f"  - Mensajes usuario: {analytics.user_messages}")
        print(f"  - Temas encontrados: {len(analytics.most_common_topics)}")
        print(f"  - Respuestas encontradas: {len(analytics.most_common_responses)}")
        
        if analytics.most_common_topics:
            print(f"📊 ANALYTICS: Primeros 5 temas:")
            for i, topic in enumerate(analytics.most_common_topics[:5], 1):
                print(f"    {i}. '{topic['palabra']}' - {topic['frecuencia']} veces")
        
        if analytics.most_common_responses:
            print(f"📊 ANALYTICS: Primeras 3 respuestas:")
            for i, response in enumerate(analytics.most_common_responses[:3], 1):
                print(f"    {i}. '{response['respuesta'][:50]}...' - {response['frecuencia']} veces")
        
        response_data = {
            'total_conversaciones': analytics.total_conversations,
            'conversaciones_activas': analytics.active_conversations,
            'total_mensajes': analytics.total_messages,
            'mensajes_usuario': analytics.user_messages,
            'mensajes_bot': analytics.bot_messages,
            'promedio_mensajes_por_conversacion': analytics.avg_messages_per_conversation,
            'temas_mas_preguntados': analytics.most_common_topics,
            'respuestas_mas_frecuentes': analytics.most_common_responses,
            'conversaciones_por_dia': analytics.conversations_by_day,
            'tiempo_promedio_respuesta': analytics.response_time_stats,
            'periodo_dias': days
        }
        
        print(f"✅ ANALYTICS: Enviando respuesta con {len(response_data['temas_mas_preguntados'])} temas")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ ANALYTICS ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/combined', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_combined_analytics():
    """Obtener analítica combinada"""
    try:
        days = int(request.args.get('days', 30))
        analytics = obtener_analytics_combinados_use_case.ejecutar(days)
        
        return jsonify(analytics)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/messages', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_message_analytics():
    """Obtener analítica de mensajes"""
    try:
        days = int(request.args.get('days', 30))
        analytics = obtener_analytics_mensajes_use_case.ejecutar(days)
        
        return jsonify({
            'total_mensajes': analytics.total_messages,
            'mensajes_por_rol': analytics.messages_by_role,
            'mensajes_por_dia': analytics.messages_by_day,
            'longitud_promedio': analytics.avg_message_length,
            'palabras_mas_comunes': analytics.most_common_words,
            'periodo_dias': days
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
