from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from funcionalidades.core.infraestructura.database import db
from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.rag.infrastructure.embedder_openai import OpenAIEmbedder


class ConversationService:
    """Servicio para manejar conversaciones persistentes con resumen automático"""
    
    def __init__(self):
        self.embedder = OpenAIEmbedder()
        self.MAX_MESSAGES_BEFORE_SUMMARY = 10
    
    def get_or_create_conversation(self, user_id: Optional[int] = None, session_id: Optional[str] = None) -> ConversationModel:
        """Obtener o crear una conversación activa"""
        # Buscar conversación activa existente
        conversation = ConversationModel.query.filter_by(
            user_id=user_id,
            session_id=session_id,
            is_active=True
        ).first()
        
        if not conversation:
            # Crear nueva conversación
            conversation = ConversationModel(
                user_id=user_id,
                session_id=session_id,
                title=self._generate_conversation_title(),
                is_active=True
            )
            db.session.add(conversation)
            db.session.commit()
        
        return conversation
    
    def add_message(self, conversation_id: int, role: str, content: str, user_id: Optional[int] = None) -> ChatMessageModel:
        """Agregar mensaje a una conversación"""
        conversation = ConversationModel.query.get(conversation_id)
        if not conversation:
            raise ValueError("Conversación no encontrada")
        
        # Crear mensaje
        message = ChatMessageModel(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        db.session.add(message)
        
        # Actualizar contador y última actividad
        conversation.message_count += 1
        conversation.last_message_at = datetime.utcnow()
        
        # Verificar si necesita resumen
        if conversation.message_count % self.MAX_MESSAGES_BEFORE_SUMMARY == 0:
            self._summarize_conversation(conversation)
        
        db.session.commit()
        return message
    
    def get_conversation_messages(self, conversation_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener mensajes de una conversación"""
        messages = ChatMessageModel.query.filter_by(
            conversation_id=conversation_id
        ).order_by(ChatMessageModel.created_at.asc()).limit(limit).all()
        
        return [
            {
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'created_at': msg.created_at.isoformat()
            }
            for msg in messages
        ]
    
    def get_user_conversations(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Obtener conversaciones de un usuario"""
        conversations = ConversationModel.query.filter_by(
            user_id=user_id
        ).order_by(ConversationModel.last_message_at.desc()).limit(limit).all()
        
        return [
            {
                'id': conv.id,
                'title': conv.title,
                'summary': conv.summary,
                'message_count': conv.message_count,
                'last_message_at': conv.last_message_at.isoformat(),
                'created_at': conv.created_at.isoformat(),
                'is_active': conv.is_active
            }
            for conv in conversations
        ]
    
    def get_session_conversations(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Obtener conversaciones de una sesión anónima"""
        conversations = ConversationModel.query.filter_by(
            session_id=session_id
        ).order_by(ConversationModel.last_message_at.desc()).limit(limit).all()
        
        return [
            {
                'id': conv.id,
                'title': conv.title,
                'summary': conv.summary,
                'message_count': conv.message_count,
                'last_message_at': conv.last_message_at.isoformat(),
                'created_at': conv.created_at.isoformat(),
                'is_active': conv.is_active
            }
            for conv in conversations
        ]
    
    def close_conversation(self, conversation_id: int) -> bool:
        """Cerrar una conversación"""
        conversation = ConversationModel.query.get(conversation_id)
        if not conversation:
            return False
        
        conversation.is_active = False
        db.session.commit()
        return True
    
    def _generate_conversation_title(self) -> str:
        """Generar título automático para la conversación"""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        return f"Conversación del {timestamp}"
    
    def _summarize_conversation(self, conversation: ConversationModel) -> None:
        """Crear resumen de la conversación cuando alcanza el límite de mensajes"""
        try:
            # Obtener mensajes recientes para resumir
            recent_messages = ChatMessageModel.query.filter_by(
                conversation_id=conversation.id
            ).order_by(ChatMessageModel.created_at.desc()).limit(self.MAX_MESSAGES_BEFORE_SUMMARY).all()
            
            # Crear contexto para el resumen
            messages_text = []
            for msg in reversed(recent_messages):  # Orden cronológico
                role_name = "Usuario" if msg.role == "user" else "Asistente"
                messages_text.append(f"{role_name}: {msg.content}")
            
            context = "\n".join(messages_text)
            
            # Generar resumen simple (sin OpenAI por ahora)
            summary = self._generate_simple_summary(context)
            
            # Actualizar resumen de la conversación
            if conversation.summary:
                conversation.summary = f"{conversation.summary}\n\n--- Resumen del {datetime.now().strftime('%d/%m/%Y %H:%M')} ---\n{summary}"
            else:
                conversation.summary = summary
            
            # Limpiar mensajes antiguos (mantener solo los últimos 5)
            old_messages = ChatMessageModel.query.filter_by(
                conversation_id=conversation.id
            ).order_by(ChatMessageModel.created_at.asc()).limit(
                conversation.message_count - 5
            ).all()
            
            for msg in old_messages:
                db.session.delete(msg)
            
            # Actualizar contador
            conversation.message_count = 5
            
        except Exception as e:
            print(f"Error generando resumen: {e}")
            # Si falla el resumen, solo limpiar mensajes antiguos
            old_messages = ChatMessageModel.query.filter_by(
                conversation_id=conversation.id
            ).order_by(ChatMessageModel.created_at.asc()).limit(
                conversation.message_count - 5
            ).all()
            
            for msg in old_messages:
                db.session.delete(msg)
            
            conversation.message_count = 5
    
    def _generate_simple_summary(self, context: str) -> str:
        """Generar resumen simple de la conversación"""
        lines = context.split('\n')
        user_messages = [line for line in lines if line.startswith('Usuario:')]
        assistant_messages = [line for line in lines if line.startswith('Asistente:')]
        
        # Crear resumen básico
        summary_parts = []
        
        if user_messages:
            summary_parts.append(f"Usuario hizo {len(user_messages)} consultas")
            # Tomar las primeras palabras de las primeras consultas
            first_queries = []
            for msg in user_messages[:3]:
                content = msg.replace('Usuario: ', '')
                if len(content) > 50:
                    content = content[:50] + "..."
                first_queries.append(content)
            summary_parts.append(f"Temas principales: {', '.join(first_queries)}")
        
        if assistant_messages:
            summary_parts.append(f"Asistente respondió {len(assistant_messages)} veces")
        
        return " | ".join(summary_parts) if summary_parts else "Conversación resumida"
