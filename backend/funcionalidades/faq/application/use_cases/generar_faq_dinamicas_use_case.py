from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import Counter
import re

from funcionalidades.faq.domain.entities.faq_entity import FAQ
from funcionalidades.faq.domain.repositories.faq_repository import FAQRepository
from funcionalidades.core.infraestructura.database import db
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.chatlog.infrastructure.conversation_model import ConversationModel


class GenerarFAQDinamicasUseCase:
    def __init__(self, faq_repo: FAQRepository):
        self.faq_repo = faq_repo

    def ejecutar(self, dias_atras: int = 30) -> List[FAQ]:
        """
        Generar preguntas frecuentes basadas en conversaciones reales de usuarios
        Incluye tanto conversaciones activas como inactivas para tener historial completo
        """
        print(f"🔍 FAQ DINÁMICAS: Generando FAQ basadas en conversaciones de los últimos {dias_atras} días")
        
        # Calcular fecha de inicio
        fecha_inicio = datetime.utcnow() - timedelta(days=dias_atras)
        
        # Obtener todas las preguntas de usuarios (incluyendo conversaciones inactivas)
        user_questions = db.session.query(ChatMessageModel.content).join(ConversationModel).filter(
            ChatMessageModel.role == 'user',
            ChatMessageModel.created_at >= fecha_inicio
        ).all()
        
        print(f"📊 FAQ DINÁMICAS: Encontradas {len(user_questions)} preguntas de usuarios")
        
        if not user_questions:
            print("📊 FAQ DINÁMICAS: No hay preguntas suficientes para generar FAQ dinámicas")
            return []
        
        # Procesar y agrupar preguntas similares
        processed_questions = self._process_questions([q[0] for q in user_questions])
        
        # Generar FAQ dinámicas
        dynamic_faqs = self._generate_dynamic_faqs(processed_questions)
        
        print(f"✅ FAQ DINÁMICAS: Generadas {len(dynamic_faqs)} preguntas frecuentes dinámicas")
        
        return dynamic_faqs

    def _process_questions(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Procesar y agrupar preguntas similares"""
        print(f"🔤 FAQ DINÁMICAS: Procesando {len(questions)} preguntas")
        
        # Filtrar preguntas válidas
        valid_questions = []
        for question in questions:
            clean_question = question.strip()
            if (len(clean_question) > 10 and  # Mínimo 10 caracteres
                len(clean_question) < 200 and  # Máximo 200 caracteres
                not re.match(r'^[^\w]*$', clean_question)):  # No solo símbolos
                valid_questions.append(clean_question)
        
        print(f"🔤 FAQ DINÁMICAS: {len(valid_questions)} preguntas válidas después del filtrado")
        
        # Agrupar preguntas similares
        question_groups = {}
        for question in valid_questions:
            normalized = self._normalize_question(question)
            found_group = False
            
            for group_key in question_groups:
                if self._are_questions_similar(normalized, group_key):
                    question_groups[group_key].append(question)
                    found_group = True
                    break
            
            if not found_group:
                question_groups[normalized] = [question]
        
        # Convertir a lista con conteos
        result = []
        for group_key, questions_list in question_groups.items():
            if len(questions_list) >= 2:  # Solo grupos con 2+ preguntas similares
                result.append({
                    'representative': questions_list[0],  # Usar la primera como representante
                    'count': len(questions_list),
                    'all_questions': questions_list
                })
        
        # Ordenar por frecuencia
        result.sort(key=lambda x: x['count'], reverse=True)
        
        print(f"📊 FAQ DINÁMICAS: {len(result)} grupos de preguntas similares encontrados")
        return result

    def _normalize_question(self, question: str) -> str:
        """Normalizar pregunta para comparación"""
        # Convertir a minúsculas
        normalized = question.lower()
        
        # Remover signos de puntuación
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        
        # Remover palabras comunes
        stop_words = {
            'hola', 'buenos', 'días', 'tardes', 'noches', 'gracias', 'por', 'favor',
            'disculpe', 'disculpa', 'perdón', 'perdone', 'ayuda', 'necesito', 'quiero',
            'puedo', 'podría', 'me', 'mi', 'mí', 'con', 'para', 'sobre', 'acerca',
            'de', 'del', 'la', 'el', 'las', 'los', 'un', 'una', 'uno', 'unas', 'unos',
            'es', 'son', 'está', 'están', 'tiene', 'tienen', 'hay', 'cómo', 'cuándo',
            'dónde', 'qué', 'quién', 'cuál', 'cuáles', 'por', 'qué', 'para', 'qué'
        }
        
        words = normalized.split()
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return ' '.join(filtered_words)

    def _are_questions_similar(self, question1: str, question2: str) -> bool:
        """Determinar si dos preguntas son similares"""
        words1 = set(question1.split())
        words2 = set(question2.split())
        
        if not words1 or not words2:
            return False
        
        # Calcular similitud basada en palabras comunes
        common_words = words1.intersection(words2)
        similarity = len(common_words) / max(len(words1), len(words2))
        
        return similarity > 0.6  # 60% de similitud

    def _generate_dynamic_faqs(self, question_groups: List[Dict[str, Any]]) -> List[FAQ]:
        """Generar FAQ dinámicas basadas en grupos de preguntas"""
        dynamic_faqs = []
        
        # Obtener FAQ estáticas existentes para evitar duplicados
        existing_faqs = self.faq_repo.listar()
        existing_questions = {faq.pregunta.lower() for faq in existing_faqs}
        
        for i, group in enumerate(question_groups[:10], 1):  # Máximo 10 FAQ dinámicas
            representative = group['representative']
            count = group['count']
            
            # Verificar que no sea similar a FAQ existentes
            if not any(self._are_questions_similar(representative.lower(), existing.lower()) 
                      for existing in existing_questions):
                
                # Generar respuesta basada en el contexto
                answer = self._generate_answer_for_question(representative, count)
                
                if answer:
                    faq = FAQ(
                        id=1000 + i,  # IDs altos para FAQ dinámicas
                        pregunta=representative,
                        respuesta=answer
                    )
                    dynamic_faqs.append(faq)
                    existing_questions.add(representative.lower())
        
        return dynamic_faqs

    def _generate_answer_for_question(self, question: str, frequency: int) -> str:
        """Generar respuesta para una pregunta frecuente"""
        question_lower = question.lower()
        
        # Respuestas basadas en patrones comunes
        if any(word in question_lower for word in ['envío', 'enviar', 'entrega', 'llegar']):
            return f"Basado en {frequency} consultas similares: Ofrecemos envío estándar (3-5 días hábiles) y envío express (1-2 días hábiles). Los costos varían según el destino y peso del paquete."
        
        elif any(word in question_lower for word in ['devolver', 'devolución', 'cambiar', 'cambio']):
            return f"Basado en {frequency} consultas similares: Tienes 30 días calendario desde la fecha de entrega para devolver cualquier producto en perfecto estado. El producto debe estar en su empaque original."
        
        elif any(word in question_lower for word in ['rastrear', 'seguimiento', 'dónde', 'estado']):
            return f"Basado en {frequency} consultas similares: Una vez que tu pedido sea enviado, recibirás un email con el número de seguimiento. También puedes consultar el estado en tu cuenta."
        
        elif any(word in question_lower for word in ['pago', 'pagar', 'tarjeta', 'método']):
            return f"Basado en {frequency} consultas similares: Aceptamos tarjetas de crédito/débito (Visa, Mastercard, American Express), PayPal y transferencias bancarias."
        
        elif any(word in question_lower for word in ['cancelar', 'modificar', 'cambiar pedido']):
            return f"Basado en {frequency} consultas similares: Puedes modificar o cancelar tu pedido hasta 2 horas después de realizarlo, siempre que no haya sido procesado para envío."
        
        elif any(word in question_lower for word in ['precio', 'costo', 'cuánto', 'vale']):
            return f"Basado en {frequency} consultas similares: Los precios varían según el producto. Puedes ver los precios actualizados en nuestro catálogo. Para información específica, contacta a soporte@arrozales.com"
        
        elif any(word in question_lower for word in ['producto', 'artículo', 'disponible', 'stock']):
            return f"Basado en {frequency} consultas similares: Puedes consultar la disponibilidad de productos en nuestro catálogo. Si un producto no está disponible, puedes contactarnos para más información."
        
        elif any(word in question_lower for word in ['contacto', 'soporte', 'ayuda', 'problema']):
            return f"Basado en {frequency} consultas similares: Para soporte técnico o consultas específicas, puedes contactarnos en soporte@arrozales.com o crear un ticket de soporte desde tu cuenta."
        
        else:
            # Respuesta genérica para preguntas no categorizadas
            return f"Basado en {frequency} consultas similares: Esta es una pregunta frecuente de nuestros usuarios. Para una respuesta más específica, te recomendamos contactar a nuestro equipo de soporte en soporte@arrozales.com"
