from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import Counter
import re
from funcionalidades.core.infraestructura.database import db
from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel


class ConversationAnalyticsService:
    """Servicio para analítica de conversaciones y tickets"""
    
    def __init__(self):
        pass
    
    def get_conversation_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Obtener analítica básica de conversaciones"""
        try:
            # Fecha de inicio
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Total de conversaciones
            total_conversations = ConversationModel.query.filter(
                ConversationModel.created_at >= start_date
            ).count()
            
            # Conversaciones activas
            active_conversations = ConversationModel.query.filter(
                ConversationModel.is_active == True,
                ConversationModel.created_at >= start_date
            ).count()
            
            # Total de mensajes
            total_messages = ChatMessageModel.query.filter(
                ChatMessageModel.created_at >= start_date
            ).count()
            
            # Mensajes por tipo
            user_messages = ChatMessageModel.query.filter(
                ChatMessageModel.role == 'user',
                ChatMessageModel.created_at >= start_date
            ).count()
            
            bot_messages = ChatMessageModel.query.filter(
                ChatMessageModel.role == 'assistant',
                ChatMessageModel.created_at >= start_date
            ).count()
            
            # Temas más preguntados (palabras clave en mensajes de usuario)
            user_messages_content = db.session.query(ChatMessageModel.content).filter(
                ChatMessageModel.role == 'user',
                ChatMessageModel.created_at >= start_date
            ).all()
            
            # Extraer palabras clave
            keywords = self._extract_keywords([msg[0] for msg in user_messages_content])
            
            # Respuestas más frecuentes del bot
            bot_responses = db.session.query(ChatMessageModel.content).filter(
                ChatMessageModel.role == 'assistant',
                ChatMessageModel.created_at >= start_date
            ).all()
            
            frequent_responses = self._get_frequent_responses([msg[0] for msg in bot_responses])
            
            # Conversaciones por día
            daily_conversations = self._get_daily_conversations(days)
            
            # Tiempo promedio de respuesta
            avg_response_time = self._calculate_avg_response_time(start_date)
            
            return {
                'periodo_dias': days,
                'total_conversaciones': total_conversations,
                'conversaciones_activas': active_conversations,
                'total_mensajes': total_messages,
                'mensajes_usuario': user_messages,
                'mensajes_bot': bot_messages,
                'temas_mas_preguntados': keywords[:10],  # Top 10
                'respuestas_mas_frecuentes': frequent_responses[:10],  # Top 10
                'conversaciones_por_dia': daily_conversations,
                'tiempo_promedio_respuesta': avg_response_time,
                'fecha_analisis': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error en analítica de conversaciones: {e}")
            return {
                'error': str(e),
                'periodo_dias': days,
                'total_conversaciones': 0,
                'conversaciones_activas': 0,
                'total_mensajes': 0,
                'mensajes_usuario': 0,
                'mensajes_bot': 0,
                'temas_mas_preguntados': [],
                'respuestas_mas_frecuentes': [],
                'conversaciones_por_dia': [],
                'tiempo_promedio_respuesta': 0,
                'fecha_analisis': datetime.utcnow().isoformat()
            }
    
    def get_ticket_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Obtener analítica de tickets"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Total de tickets
            total_tickets = TicketModel.query.filter(
                TicketModel.created_at >= start_date
            ).count()
            
            # Tickets por estado
            tickets_abiertos = TicketModel.query.filter(
                TicketModel.status == 'abierto',
                TicketModel.created_at >= start_date
            ).count()
            
            tickets_en_progreso = TicketModel.query.filter(
                TicketModel.status == 'en_progreso',
                TicketModel.created_at >= start_date
            ).count()
            
            tickets_cerrados = TicketModel.query.filter(
                TicketModel.status == 'cerrado',
                TicketModel.created_at >= start_date
            ).count()
            
            tickets_resueltos = TicketModel.query.filter(
                TicketModel.status == 'resuelto',
                TicketModel.created_at >= start_date
            ).count()
            
            # Tickets por prioridad
            tickets_urgentes = TicketModel.query.filter(
                TicketModel.priority == 'urgente',
                TicketModel.created_at >= start_date
            ).count()
            
            tickets_altos = TicketModel.query.filter(
                TicketModel.priority == 'alta',
                TicketModel.created_at >= start_date
            ).count()
            
            # Tiempo promedio de resolución
            resolved_tickets = TicketModel.query.filter(
                TicketModel.status.in_(['cerrado', 'resuelto']),
                TicketModel.created_at >= start_date,
                TicketModel.closed_at.isnot(None)
            ).all()
            
            resolution_times = []
            for ticket in resolved_tickets:
                if ticket.closed_at:
                    diff = ticket.closed_at - ticket.created_at
                    resolution_times.append(diff.total_seconds() / 3600)  # en horas
            
            avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
            
            # Tickets por categoría
            categories = db.session.query(
                TicketModel.category,
                db.func.count(TicketModel.id)
            ).filter(
                TicketModel.created_at >= start_date
            ).group_by(TicketModel.category).all()
            
            return {
                'periodo_dias': days,
                'total_tickets': total_tickets,
                'tickets_abiertos': tickets_abiertos,
                'tickets_en_progreso': tickets_en_progreso,
                'tickets_cerrados': tickets_cerrados,
                'tickets_resueltos': tickets_resueltos,
                'tickets_urgentes': tickets_urgentes,
                'tickets_altos': tickets_altos,
                'tiempo_promedio_resolucion_horas': round(avg_resolution_time, 2),
                'tickets_por_categoria': dict(categories),
                'fecha_analisis': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error en analítica de tickets: {e}")
            return {
                'error': str(e),
                'periodo_dias': days,
                'total_tickets': 0,
                'tickets_abiertos': 0,
                'tickets_en_progreso': 0,
                'tickets_cerrados': 0,
                'tickets_resueltos': 0,
                'tickets_urgentes': 0,
                'tickets_altos': 0,
                'tiempo_promedio_resolucion_horas': 0,
                'tickets_por_categoria': {},
                'fecha_analisis': datetime.utcnow().isoformat()
            }
    
    def _extract_keywords(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Extraer palabras clave de los mensajes"""
        # Palabras comunes a ignorar
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'pero', 'sus', 'le', 'ha', 'me', 'si', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'sido', 'puede', 'todos', 'así', 'muy', 'más', 'hasta', 'desde', 'hacer', 'pero', 'cada', 'donde', 'quien', 'con', 'entre', 'sin', 'sobre', 'tras', 'durante', 'mediante', 'excepto', 'salvo', 'menos', 'más', 'muy', 'mucho', 'poco', 'todo', 'nada', 'algo', 'alguien', 'nadie', 'alguno', 'ninguno', 'otro', 'mismo', 'tal', 'cual', 'cuanto', 'tanto', 'bastante', 'demasiado', 'suficiente', 'necesario', 'posible', 'imposible', 'probable', 'seguro', 'cierto', 'falso', 'verdadero', 'bueno', 'malo', 'mejor', 'peor', 'grande', 'pequeño', 'alto', 'bajo', 'largo', 'corto', 'ancho', 'estrecho', 'gordo', 'delgado', 'gordo', 'flaco', 'joven', 'viejo', 'nuevo', 'viejo', 'limpio', 'sucio', 'rico', 'pobre', 'fácil', 'difícil', 'simple', 'complejo', 'rápido', 'lento', 'temprano', 'tarde', 'pronto', 'lejos', 'cerca', 'dentro', 'fuera', 'arriba', 'abajo', 'delante', 'detrás', 'izquierda', 'derecha', 'norte', 'sur', 'este', 'oeste'
        }
        
        # Unir todos los mensajes
        all_text = ' '.join(messages).lower()
        
        # Extraer palabras (solo letras, mínimo 3 caracteres)
        words = re.findall(r'\b[a-záéíóúñü]{3,}\b', all_text)
        
        # Filtrar palabras comunes
        filtered_words = [word for word in words if word not in stop_words]
        
        # Contar frecuencia
        word_count = Counter(filtered_words)
        
        # Retornar top palabras con su frecuencia
        return [{'palabra': word, 'frecuencia': count} for word, count in word_count.most_common(20)]
    
    def _get_frequent_responses(self, responses: List[str]) -> List[Dict[str, Any]]:
        """Obtener respuestas más frecuentes del bot"""
        # Agrupar respuestas similares (simplificado)
        response_count = Counter(responses)
        
        # Retornar respuestas más frecuentes
        return [{'respuesta': resp, 'frecuencia': count} for resp, count in response_count.most_common(10)]
    
    def _get_daily_conversations(self, days: int) -> List[Dict[str, Any]]:
        """Obtener conversaciones por día"""
        daily_data = []
        
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=i)
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            count = ConversationModel.query.filter(
                ConversationModel.created_at >= start_of_day,
                ConversationModel.created_at < end_of_day
            ).count()
            
            daily_data.append({
                'fecha': start_of_day.strftime('%Y-%m-%d'),
                'conversaciones': count
            })
        
        return list(reversed(daily_data))  # Orden cronológico
    
    def _calculate_avg_response_time(self, start_date: datetime) -> float:
        """Calcular tiempo promedio de respuesta en minutos"""
        try:
            # Obtener pares de mensajes usuario-bot consecutivos
            messages = ChatMessageModel.query.filter(
                ChatMessageModel.created_at >= start_date
            ).order_by(ConversationModel.id, ChatMessageModel.created_at).all()
            
            response_times = []
            last_user_message = None
            
            for message in messages:
                if message.role == 'user':
                    last_user_message = message
                elif message.role == 'assistant' and last_user_message and message.conversation_id == last_user_message.conversation_id:
                    # Calcular diferencia de tiempo
                    diff = message.created_at - last_user_message.created_at
                    response_times.append(diff.total_seconds() / 60)  # en minutos
                    last_user_message = None
            
            return round(sum(response_times) / len(response_times), 2) if response_times else 0
            
        except Exception as e:
            print(f"Error calculando tiempo de respuesta: {e}")
            return 0







