from datetime import datetime, timedelta
from typing import Dict, Any, List
from collections import Counter
import re

from funcionalidades.core.infraestructura.database import db
from funcionalidades.analytics.domain.entities.conversation_analytics_entity import (
    ConversationAnalytics, TicketAnalytics, MessageAnalytics
)
from funcionalidades.analytics.domain.repositories.analytics_repository import AnalyticsRepository
from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel


class AnalyticsRepositoryImpl(AnalyticsRepository):
    def get_conversation_analytics(self, start_date: datetime, end_date: datetime) -> ConversationAnalytics:
        # Total de conversaciones (solo activas, excluyendo borradas)
        total_conversations = ConversationModel.query.filter(
            ConversationModel.created_at >= start_date,
            ConversationModel.is_active == True
        ).count()
        
        # Conversaciones activas
        active_conversations = ConversationModel.query.filter(
            ConversationModel.is_active == True,
            ConversationModel.created_at >= start_date
        ).count()
        
        # Total de mensajes (solo de conversaciones activas)
        total_messages = db.session.query(ChatMessageModel).join(ConversationModel).filter(
            ChatMessageModel.created_at >= start_date,
            ConversationModel.is_active == True
        ).count()
        
        # Mensajes por tipo (solo de conversaciones activas)
        user_messages = db.session.query(ChatMessageModel).join(ConversationModel).filter(
            ChatMessageModel.role == 'user',
            ChatMessageModel.created_at >= start_date,
            ConversationModel.is_active == True
        ).count()
        
        bot_messages = db.session.query(ChatMessageModel).join(ConversationModel).filter(
            ChatMessageModel.role == 'assistant',
            ChatMessageModel.created_at >= start_date,
            ConversationModel.is_active == True
        ).count()
        
        # Promedio de mensajes por conversación
        avg_messages_per_conversation = total_messages / total_conversations if total_conversations > 0 else 0
        
        # Temas más preguntados (solo de conversaciones activas)
        user_messages_content = db.session.query(ChatMessageModel.content).join(ConversationModel).filter(
            ChatMessageModel.role == 'user',
            ChatMessageModel.created_at >= start_date,
            ConversationModel.is_active == True
        ).all()
        
        print(f"🔍 ANALYTICS REPO: Encontrados {len(user_messages_content)} mensajes de usuario (solo conversaciones activas)")
        if user_messages_content:
            print(f"📝 ANALYTICS REPO: Primeros 3 mensajes:")
            for i, msg in enumerate(user_messages_content[:3], 1):
                print(f"    {i}. {msg[0][:50]}...")
        
        most_common_topics = self._extract_keywords([msg[0] for msg in user_messages_content])
        print(f"📊 ANALYTICS REPO: Extraídos {len(most_common_topics)} temas")
        
        # Respuestas más frecuentes del bot (solo de conversaciones activas)
        bot_messages_content = db.session.query(ChatMessageModel.content).join(ConversationModel).filter(
            ChatMessageModel.role == 'assistant',
            ChatMessageModel.created_at >= start_date,
            ConversationModel.is_active == True
        ).all()
        
        print(f"🔍 ANALYTICS REPO: Encontrados {len(bot_messages_content)} mensajes del bot (solo conversaciones activas)")
        if bot_messages_content:
            print(f"📝 ANALYTICS REPO: Primeros 3 mensajes del bot:")
            for i, msg in enumerate(bot_messages_content[:3], 1):
                print(f"    {i}. {msg[0][:50]}...")
        
        most_common_responses = self._extract_common_responses([msg[0] for msg in bot_messages_content])
        print(f"📊 ANALYTICS REPO: Extraídas {len(most_common_responses)} respuestas frecuentes")
        
        # Conversaciones por día
        conversations_by_day = self._get_daily_conversations(start_date, end_date)
        
        # Tiempo promedio de respuesta
        response_time_stats = self._calculate_avg_response_time(start_date)
        
        return ConversationAnalytics(
            total_conversations=total_conversations,
            active_conversations=active_conversations,
            total_messages=total_messages,
            user_messages=user_messages,
            bot_messages=bot_messages,
            avg_messages_per_conversation=avg_messages_per_conversation,
            most_common_topics=most_common_topics[:10],
            most_common_responses=most_common_responses[:10],
            conversations_by_day=conversations_by_day,
            response_time_stats=response_time_stats
        )

    def get_ticket_analytics(self, start_date: datetime, end_date: datetime) -> TicketAnalytics:
        # Total de tickets
        total_tickets = TicketModel.query.filter(
            TicketModel.created_at >= start_date
        ).count()
        
        # Tickets por estado
        open_tickets = TicketModel.query.filter(
            TicketModel.status == 'abierto',
            TicketModel.created_at >= start_date
        ).count()
        
        closed_tickets = TicketModel.query.filter(
            TicketModel.status == 'cerrado',
            TicketModel.created_at >= start_date
        ).count()
        
        resolved_tickets = TicketModel.query.filter(
            TicketModel.status == 'resuelto',
            TicketModel.created_at >= start_date
        ).count()
        
        # Tickets por prioridad
        tickets_by_priority = {
            'urgente': TicketModel.query.filter(
                TicketModel.priority == 'urgente',
                TicketModel.created_at >= start_date
            ).count(),
            'alta': TicketModel.query.filter(
                TicketModel.priority == 'alta',
                TicketModel.created_at >= start_date
            ).count(),
            'media': TicketModel.query.filter(
                TicketModel.priority == 'media',
                TicketModel.created_at >= start_date
            ).count(),
            'baja': TicketModel.query.filter(
                TicketModel.priority == 'baja',
                TicketModel.created_at >= start_date
            ).count()
        }
        
        # Tickets por categoría
        tickets_by_category = {}
        categories = db.session.query(TicketModel.category).filter(
            TicketModel.created_at >= start_date
        ).distinct().all()
        
        for category in categories:
            if category[0]:
                tickets_by_category[category[0]] = TicketModel.query.filter(
                    TicketModel.category == category[0],
                    TicketModel.created_at >= start_date
                ).count()
        
        # Tickets por estado
        tickets_by_status = {
            'abierto': open_tickets,
            'en_progreso': TicketModel.query.filter(
                TicketModel.status == 'en_progreso',
                TicketModel.created_at >= start_date
            ).count(),
            'cerrado': closed_tickets,
            'resuelto': resolved_tickets
        }
        
        # Tiempo promedio de resolución
        resolved_tickets_with_time = TicketModel.query.filter(
            TicketModel.status.in_(['cerrado', 'resuelto']),
            TicketModel.created_at >= start_date,
            TicketModel.closed_at.isnot(None)
        ).all()
        
        total_resolution_time = 0
        for ticket in resolved_tickets_with_time:
            if ticket.closed_at and ticket.created_at:
                resolution_time = (ticket.closed_at - ticket.created_at).total_seconds() / 3600  # horas
                total_resolution_time += resolution_time
        
        avg_resolution_time = total_resolution_time / len(resolved_tickets_with_time) if resolved_tickets_with_time else 0
        
        # Tickets por día
        tickets_by_day = self._get_daily_tickets(start_date, end_date)
        
        return TicketAnalytics(
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            closed_tickets=closed_tickets,
            resolved_tickets=resolved_tickets,
            tickets_by_priority=tickets_by_priority,
            tickets_by_category=tickets_by_category,
            tickets_by_status=tickets_by_status,
            avg_resolution_time=avg_resolution_time,
            tickets_by_day=tickets_by_day
        )

    def get_message_analytics(self, start_date: datetime, end_date: datetime) -> MessageAnalytics:
        # Total de mensajes
        total_messages = ChatMessageModel.query.filter(
            ChatMessageModel.created_at >= start_date
        ).count()
        
        # Mensajes por rol
        messages_by_role = {
            'user': ChatMessageModel.query.filter(
                ChatMessageModel.role == 'user',
                ChatMessageModel.created_at >= start_date
            ).count(),
            'assistant': ChatMessageModel.query.filter(
                ChatMessageModel.role == 'assistant',
                ChatMessageModel.created_at >= start_date
            ).count(),
            'system': ChatMessageModel.query.filter(
                ChatMessageModel.role == 'system',
                ChatMessageModel.created_at >= start_date
            ).count()
        }
        
        # Mensajes por día
        messages_by_day = self._get_daily_messages(start_date, end_date)
        
        # Longitud promedio de mensajes
        messages = db.session.query(ChatMessageModel.content).filter(
            ChatMessageModel.created_at >= start_date
        ).all()
        
        total_length = sum(len(msg[0] or '') for msg in messages)
        avg_message_length = total_length / len(messages) if messages else 0
        
        # Palabras más comunes
        all_content = [msg[0] or '' for msg in messages]
        most_common_words = self._extract_keywords(all_content)
        
        return MessageAnalytics(
            total_messages=total_messages,
            messages_by_role=messages_by_role,
            messages_by_day=messages_by_day,
            avg_message_length=avg_message_length,
            most_common_words=most_common_words[:20]
        )

    def get_combined_analytics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        conversation_analytics = self.get_conversation_analytics(start_date, end_date)
        ticket_analytics = self.get_ticket_analytics(start_date, end_date)
        message_analytics = self.get_message_analytics(start_date, end_date)
        
        return {
            'conversaciones': {
                'total': conversation_analytics.total_conversations,
                'activas': conversation_analytics.active_conversations,
                'mensajes_totales': conversation_analytics.total_messages,
                'mensajes_usuario': conversation_analytics.user_messages,
                'mensajes_bot': conversation_analytics.bot_messages,
                'promedio_mensajes_por_conversacion': conversation_analytics.avg_messages_per_conversation,
                'temas_mas_preguntados': conversation_analytics.most_common_topics,
                'conversaciones_por_dia': conversation_analytics.conversations_by_day,
                'tiempo_promedio_respuesta': conversation_analytics.response_time_stats
            },
            'tickets': {
                'total': ticket_analytics.total_tickets,
                'abiertos': ticket_analytics.open_tickets,
                'cerrados': ticket_analytics.closed_tickets,
                'resueltos': ticket_analytics.resolved_tickets,
                'por_prioridad': ticket_analytics.tickets_by_priority,
                'por_categoria': ticket_analytics.tickets_by_category,
                'por_estado': ticket_analytics.tickets_by_status,
                'tiempo_promedio_resolucion': ticket_analytics.avg_resolution_time,
                'tickets_por_dia': ticket_analytics.tickets_by_day
            },
            'mensajes': {
                'total': message_analytics.total_messages,
                'por_rol': message_analytics.messages_by_role,
                'por_dia': message_analytics.messages_by_day,
                'longitud_promedio': message_analytics.avg_message_length,
                'palabras_mas_comunes': message_analytics.most_common_words
            },
            'fecha_analisis': datetime.utcnow().isoformat()
        }

    def _extract_keywords(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Extraer palabras clave de los mensajes"""
        print(f"🔍 KEYWORDS: Procesando {len(messages)} mensajes")
        
        # Palabras comunes a ignorar
        stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'pero', 'sus', 'muy', 'más', 'también', 'todo', 'todos', 'toda', 'todas', 'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'aquel', 'aquella', 'aquellos', 'aquellas', 'me', 'mi', 'mis', 'tu', 'tus', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'su', 'sus', 'suyo', 'suya', 'suyos', 'suyas', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras'}
        
        # Combinar todos los mensajes
        all_text = ' '.join(messages).lower()
        print(f"📝 KEYWORDS: Texto combinado ({len(all_text)} caracteres): {all_text[:100]}...")
        
        # Extraer palabras (solo letras, mínimo 3 caracteres)
        words = re.findall(r'\b[a-záéíóúñü]{3,}\b', all_text)
        print(f"🔤 KEYWORDS: Extraídas {len(words)} palabras")
        
        # Filtrar palabras comunes y contar
        filtered_words = [word for word in words if word not in stop_words]
        print(f"🔤 KEYWORDS: Después de filtrar stop words: {len(filtered_words)} palabras")
        
        word_counts = Counter(filtered_words)
        
        # Convertir a lista de diccionarios
        result = [{'palabra': word, 'frecuencia': count} for word, count in word_counts.most_common(20)]
        print(f"📊 KEYWORDS: Resultado final: {len(result)} temas")
        
        if result:
            print(f"📊 KEYWORDS: Primeros 5 temas:")
            for i, topic in enumerate(result[:5], 1):
                print(f"    {i}. '{topic['palabra']}' - {topic['frecuencia']} veces")
        
        return result

    def _extract_common_responses(self, responses: List[str]) -> List[Dict[str, Any]]:
        """Extraer respuestas más frecuentes del bot"""
        print(f"🔍 RESPONSES: Procesando {len(responses)} respuestas del bot")
        
        if not responses:
            print("📊 RESPONSES: No hay respuestas para procesar")
            return []
        
        # Filtrar y normalizar respuestas
        filtered_responses = []
        generic_patterns = [
            r'^hola.*', r'^gracias.*', r'^de nada.*', r'^por favor.*', 
            r'^disculpa.*', r'^lo siento.*', r'^entendido.*', r'^perfecto.*',
            r'^excelente.*', r'^claro.*', r'^sí.*', r'^no.*', r'^ok.*',
            r'^bueno.*', r'^bien.*', r'^mal.*', r'^genial.*', r'^fantástico.*',
            r'^increíble.*', r'^conectado.*', r'^error.*', r'^disculpe.*'
        ]
        
        for response in responses:
            # Limpiar la respuesta
            clean_response = response.strip()
            
            # Filtrar respuestas muy cortas, muy largas o genéricas
            if (20 < len(clean_response) < 500 and 
                not any(re.match(pattern, clean_response.lower()) for pattern in generic_patterns)):
                filtered_responses.append(clean_response)
        
        print(f"🔤 RESPONSES: Después de filtrar: {len(filtered_responses)} respuestas")
        
        if not filtered_responses:
            print("📊 RESPONSES: No hay respuestas válidas después del filtrado")
            return []
        
        # Agrupar respuestas similares usando similitud mejorada
        response_groups = {}
        
        for response in filtered_responses:
            # Normalizar para comparación
            normalized = self._normalize_response(response)
            
            # Buscar grupo similar existente
            found_group = False
            for group_key in response_groups:
                if self._are_responses_similar(normalized, group_key):
                    response_groups[group_key].append(response)
                    found_group = True
                    break
            
            if not found_group:
                response_groups[normalized] = [response]
        
        # Convertir a lista de diccionarios
        result = []
        for group_key, group_responses in response_groups.items():
            if len(group_responses) > 1:  # Solo grupos con más de una respuesta
                # Usar la respuesta más representativa del grupo
                representative = max(group_responses, key=len)
                result.append({
                    'respuesta': representative[:150] + '...' if len(representative) > 150 else representative,
                    'frecuencia': len(group_responses)
                })
        
        # Ordenar por frecuencia
        result.sort(key=lambda x: x['frecuencia'], reverse=True)
        
        print(f"📊 RESPONSES: Resultado final: {len(result)} respuestas frecuentes")
        
        if result:
            print(f"📊 RESPONSES: Primeras 3 respuestas:")
            for i, resp in enumerate(result[:3], 1):
                print(f"    {i}. '{resp['respuesta'][:50]}...' - {resp['frecuencia']} veces")
        
        return result
    
    def _normalize_response(self, response: str) -> str:
        """Normalizar respuesta para comparación"""
        # Convertir a minúsculas
        normalized = response.lower()
        
        # Remover caracteres especiales y espacios extra
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Remover palabras comunes que no aportan significado
        stop_words = {'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'en', 'con', 'por', 'para', 'que', 'es', 'son', 'está', 'están', 'tiene', 'tienen', 'puede', 'pueden', 'ser', 'estar', 'tener', 'hacer', 'decir', 'ver', 'saber', 'ir', 'venir', 'dar', 'tomar', 'llevar', 'traer', 'poner', 'quitar', 'abrir', 'cerrar', 'empezar', 'terminar', 'comenzar', 'acabar', 'seguir', 'continuar', 'parar', 'detener', 'buscar', 'encontrar', 'perder', 'ganar', 'comprar', 'vender', 'pagar', 'cobrar', 'gastar', 'ahorrar', 'invertir', 'trabajar', 'estudiar', 'aprender', 'enseñar', 'ayudar', 'servir', 'atender', 'cuidar', 'proteger', 'defender', 'atacar', 'luchar', 'pelear', 'discutir', 'hablar', 'conversar', 'preguntar', 'responder', 'explicar', 'entender', 'comprender', 'pensar', 'creer', 'saber', 'conocer', 'recordar', 'olvidar', 'imaginar', 'soñar', 'desear', 'querer', 'necesitar', 'preferir', 'elegir', 'decidir', 'aceptar', 'rechazar', 'aprobar', 'desaprobar', 'gustar', 'amar', 'odiar', 'temer', 'sufrir', 'disfrutar', 'divertir', 'reír', 'llorar', 'sonreír', 'gritar', 'callar', 'escuchar', 'oír', 'mirar', 'ver', 'observar', 'notar', 'darse', 'cuenta', 'realizar', 'hacer', 'crear', 'construir', 'destruir', 'romper', 'arreglar', 'reparar', 'mejorar', 'empeorar', 'cambiar', 'modificar', 'transformar', 'convertir', 'volver', 'regresar', 'volver', 'a', 'empezar', 'de', 'nuevo', 'repetir', 'continuar', 'seguir', 'adelante', 'atrás', 'arriba', 'abajo', 'dentro', 'fuera', 'aquí', 'allí', 'ahora', 'antes', 'después', 'siempre', 'nunca', 'a veces', 'mucho', 'poco', 'más', 'menos', 'muy', 'bastante', 'demasiado', 'suficiente', 'todo', 'nada', 'algo', 'alguien', 'nadie', 'todos', 'algunos', 'varios', 'muchos', 'pocos', 'cada', 'cualquier', 'otro', 'mismo', 'diferente', 'igual', 'parecido', 'similar', 'distinto', 'nuevo', 'viejo', 'joven', 'grande', 'pequeño', 'alto', 'bajo', 'largo', 'corto', 'ancho', 'estrecho', 'gordo', 'delgado', 'gordo', 'flaco', 'bonito', 'feo', 'bueno', 'malo', 'mejor', 'peor', 'fácil', 'difícil', 'simple', 'complicado', 'rápido', 'lento', 'temprano', 'tarde', 'pronto', 'lejos', 'cerca', 'dentro', 'fuera', 'arriba', 'abajo', 'delante', 'detrás', 'izquierda', 'derecha', 'norte', 'sur', 'este', 'oeste', 'centro', 'medio', 'principio', 'final', 'comienzo', 'termino', 'inicio', 'fin'}
        
        words = normalized.split()
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return ' '.join(filtered_words)
    
    def _are_responses_similar(self, response1: str, response2: str) -> bool:
        """Determinar si dos respuestas son similares"""
        # Si una está contenida en la otra (con un margen de diferencia)
        if len(response1) > 0 and len(response2) > 0:
            # Calcular similitud básica por palabras comunes
            words1 = set(response1.split())
            words2 = set(response2.split())
            
            if len(words1) > 0 and len(words2) > 0:
                common_words = words1.intersection(words2)
                similarity = len(common_words) / max(len(words1), len(words2))
                
                # Si tienen más del 60% de palabras en común, son similares
                return similarity > 0.6
        
        return False

    def _get_daily_conversations(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Obtener conversaciones por día (solo activas)"""
        daily_data = []
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        while current_date <= end_date_only:
            count = ConversationModel.query.filter(
                db.func.date(ConversationModel.created_at) == current_date,
                ConversationModel.is_active == True
            ).count()
            
            daily_data.append({
                'fecha': current_date.isoformat(),
                'conversaciones': count
            })
            
            current_date += timedelta(days=1)
        
        return daily_data

    def _get_daily_tickets(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Obtener tickets por día"""
        daily_data = []
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        while current_date <= end_date_only:
            count = TicketModel.query.filter(
                db.func.date(TicketModel.created_at) == current_date
            ).count()
            
            daily_data.append({
                'fecha': current_date.isoformat(),
                'tickets': count
            })
            
            current_date += timedelta(days=1)
        
        return daily_data

    def _get_daily_messages(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Obtener mensajes por día"""
        daily_data = []
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        while current_date <= end_date_only:
            count = ChatMessageModel.query.filter(
                db.func.date(ChatMessageModel.created_at) == current_date
            ).count()
            
            daily_data.append({
                'fecha': current_date.isoformat(),
                'mensajes': count
            })
            
            current_date += timedelta(days=1)
        
        return daily_data

    def _calculate_avg_response_time(self, start_date: datetime) -> Dict[str, Any]:
        """Calcular tiempo promedio de respuesta"""
        # Obtener conversaciones con mensajes
        conversations = ConversationModel.query.filter(
            ConversationModel.created_at >= start_date
        ).all()
        
        total_response_time = 0
        response_count = 0
        
        for conversation in conversations:
            messages = ChatMessageModel.query.filter(
                ChatMessageModel.conversation_id == conversation.id
            ).order_by(ChatMessageModel.created_at).all()
            
            for i in range(len(messages) - 1):
                if messages[i].role == 'user' and messages[i + 1].role == 'assistant':
                    response_time = (messages[i + 1].created_at - messages[i].created_at).total_seconds()
                    total_response_time += response_time
                    response_count += 1
        
        avg_response_time = total_response_time / response_count if response_count > 0 else 0
        
        return {
            'tiempo_promedio_segundos': avg_response_time,
            'tiempo_promedio_minutos': avg_response_time / 60,
            'total_respuestas': response_count
        }
