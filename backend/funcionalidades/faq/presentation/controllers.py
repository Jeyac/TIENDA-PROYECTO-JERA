from flask import Blueprint, jsonify

faq_bp = Blueprint('faq', __name__)

# Preguntas frecuentes estáticas
FAQ_DATA = [
    {
        "id": 1,
        "pregunta": "¿Cuáles son los métodos de envío disponibles?",
        "respuesta": "Ofrecemos envío estándar (3-5 días hábiles) y envío express (1-2 días hábiles). Los costos varían según el destino y peso del paquete."
    },
    {
        "id": 2,
        "pregunta": "¿Cuánto tiempo tengo para devolver un producto?",
        "respuesta": "Tienes 30 días calendario desde la fecha de entrega para devolver cualquier producto en perfecto estado. El producto debe estar en su empaque original."
    },
    {
        "id": 3,
        "pregunta": "¿Cómo puedo rastrear mi pedido?",
        "respuesta": "Una vez que tu pedido sea enviado, recibirás un email con el número de seguimiento. También puedes consultar el estado en tu cuenta."
    },
    {
        "id": 4,
        "pregunta": "¿Qué métodos de pago aceptan?",
        "respuesta": "Aceptamos tarjetas de crédito/débito (Visa, Mastercard, American Express), PayPal y transferencias bancarias."
    },
    {
        "id": 5,
        "pregunta": "¿Hacen envíos a todo el país?",
        "respuesta": "Sí, realizamos envíos a todas las ciudades principales del país. Para ubicaciones remotas, el tiempo de entrega puede ser mayor."
    },
    {
        "id": 6,
        "pregunta": "¿Puedo modificar o cancelar mi pedido?",
        "respuesta": "Puedes modificar o cancelar tu pedido hasta 2 horas después de realizarlo, siempre que no haya sido procesado para envío."
    }
]


@faq_bp.get('/')
def listar_faq():
    return jsonify(FAQ_DATA)


@faq_bp.get('/<int:faq_id>')
def obtener_faq(faq_id: int):
    faq = next((item for item in FAQ_DATA if item['id'] == faq_id), None)
    if not faq:
        return jsonify({'message': 'FAQ no encontrado'}), 404
    return jsonify(faq)




