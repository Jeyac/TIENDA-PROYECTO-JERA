from typing import List, Optional

from funcionalidades.faq.domain.entities.faq_entity import FAQ
from funcionalidades.faq.domain.repositories.faq_repository import FAQRepository


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
    def listar(self) -> List[FAQ]:
        return FAQ_DATA.copy()

    def get_by_id(self, faq_id: int) -> Optional[FAQ]:
        for faq in FAQ_DATA:
            if faq.id == faq_id:
                return faq
        return None

    def buscar_por_palabra_clave(self, palabra_clave: str) -> List[FAQ]:
        palabra_clave_lower = palabra_clave.lower()
        resultados = []
        
        for faq in FAQ_DATA:
            if (palabra_clave_lower in faq.pregunta.lower() or 
                palabra_clave_lower in faq.respuesta.lower()):
                resultados.append(faq)
        
        return resultados
