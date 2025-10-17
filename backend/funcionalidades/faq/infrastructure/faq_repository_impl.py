from typing import List, Optional

from funcionalidades.faq.domain.entities.faq_entity import FAQ
from funcionalidades.faq.domain.repositories.faq_repository import FAQRepository
from funcionalidades.faq.application.use_cases.generar_faq_dinamicas_use_case import GenerarFAQDinamicasUseCase


# Datos estáticos de FAQ
FAQ_DATA = [
    FAQ(
        id=1,
        pregunta="¿Cuáles son los métodos de envío disponibles?",
        respuesta="Ofrecemos envío estándar (3-5 días hábiles) y envío express (1-2 días hábiles). Los costos varían según el destino y peso del paquete."
    ),
    FAQ(
        id=2,
        pregunta="¿Cuánto tiempo tengo para devolver un producto?",
        respuesta="Tienes 30 días calendario desde la fecha de entrega para devolver cualquier producto en perfecto estado. El producto debe estar en su empaque original."
    ),
    FAQ(
        id=3,
        pregunta="¿Cómo puedo rastrear mi pedido?",
        respuesta="Una vez que tu pedido sea enviado, recibirás un email con el número de seguimiento. También puedes consultar el estado en tu cuenta."
    ),
    FAQ(
        id=4,
        pregunta="¿Qué métodos de pago aceptan?",
        respuesta="Aceptamos tarjetas de crédito/débito (Visa, Mastercard, American Express), PayPal y transferencias bancarias."
    ),
    FAQ(
        id=5,
        pregunta="¿Hacen envíos a todo el país?",
        respuesta="Sí, realizamos envíos a todas las ciudades principales del país. Para ubicaciones remotas, el tiempo de entrega puede ser mayor."
    ),
    FAQ(
        id=6,
        pregunta="¿Puedo modificar o cancelar mi pedido?",
        respuesta="Puedes modificar o cancelar tu pedido hasta 2 horas después de realizarlo, siempre que no haya sido procesado para envío."
    )
]


class FAQRepositoryImpl(FAQRepository):
    def __init__(self):
        self._dynamic_faq_generator = GenerarFAQDinamicasUseCase(self)

    def listar(self) -> List[FAQ]:
        """Listar FAQ estáticas + dinámicas basadas en conversaciones reales"""
        # Obtener FAQ estáticas
        static_faqs = FAQ_DATA.copy()
        
        # Generar FAQ dinámicas basadas en conversaciones reales
        try:
            dynamic_faqs = self._dynamic_faq_generator.ejecutar(dias_atras=30)
            print(f"📊 FAQ REPO: Combinando {len(static_faqs)} FAQ estáticas con {len(dynamic_faqs)} FAQ dinámicas")
            
            # Combinar FAQ estáticas y dinámicas
            all_faqs = static_faqs + dynamic_faqs
            
            # Ordenar por ID (estáticas primero, luego dinámicas)
            all_faqs.sort(key=lambda x: x.id)
            
            return all_faqs
            
        except Exception as e:
            print(f"⚠️ FAQ REPO: Error generando FAQ dinámicas: {e}")
            # En caso de error, devolver solo FAQ estáticas
            return static_faqs

    def get_by_id(self, faq_id: int) -> Optional[FAQ]:
        # Buscar en FAQ estáticas primero
        for faq in FAQ_DATA:
            if faq.id == faq_id:
                return faq
        
        # Si no se encuentra, buscar en FAQ dinámicas
        try:
            dynamic_faqs = self._dynamic_faq_generator.ejecutar(dias_atras=30)
            for faq in dynamic_faqs:
                if faq.id == faq_id:
                    return faq
        except Exception as e:
            print(f"⚠️ FAQ REPO: Error buscando FAQ dinámica {faq_id}: {e}")
        
        return None

    def buscar_por_palabra_clave(self, palabra_clave: str) -> List[FAQ]:
        palabra_clave_lower = palabra_clave.lower()
        resultados = []
        
        # Buscar en FAQ estáticas
        for faq in FAQ_DATA:
            if (palabra_clave_lower in faq.pregunta.lower() or 
                palabra_clave_lower in faq.respuesta.lower()):
                resultados.append(faq)
        
        # Buscar en FAQ dinámicas
        try:
            dynamic_faqs = self._dynamic_faq_generator.ejecutar(dias_atras=30)
            for faq in dynamic_faqs:
                if (palabra_clave_lower in faq.pregunta.lower() or 
                    palabra_clave_lower in faq.respuesta.lower()):
                    resultados.append(faq)
        except Exception as e:
            print(f"⚠️ FAQ REPO: Error buscando en FAQ dinámicas: {e}")
        
        return resultados
