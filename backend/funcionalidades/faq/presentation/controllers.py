from flask import Blueprint, jsonify, request
from funcionalidades.faq.application.use_cases.listar_faq_use_case import ListarFAQUseCase
from funcionalidades.faq.application.use_cases.obtener_faq_use_case import ObtenerFAQUseCase
from funcionalidades.faq.application.use_cases.buscar_faq_use_case import BuscarFAQUseCase
from funcionalidades.faq.infrastructure.faq_repository_impl import FAQRepositoryImpl

faq_bp = Blueprint('faq', __name__)

# Inicializar casos de uso
faq_repository = FAQRepositoryImpl()
listar_faq_use_case = ListarFAQUseCase(faq_repository)
obtener_faq_use_case = ObtenerFAQUseCase(faq_repository)
buscar_faq_use_case = BuscarFAQUseCase(faq_repository)


@faq_bp.get('/')
def listar_faq():
    """Listar todas las preguntas frecuentes"""
    try:
        faqs = listar_faq_use_case.ejecutar()
        
        # Convertir entidades a diccionarios para JSON
        faqs_data = []
        for faq in faqs:
            faqs_data.append({
                'id': faq.id,
                'pregunta': faq.pregunta,
                'respuesta': faq.respuesta
            })
        
        return jsonify(faqs_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@faq_bp.get('/<int:faq_id>')
def obtener_faq(faq_id: int):
    """Obtener una pregunta frecuente por ID"""
    try:
        faq = obtener_faq_use_case.ejecutar(faq_id)
        
        return jsonify({
            'id': faq.id,
            'pregunta': faq.pregunta,
            'respuesta': faq.respuesta
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@faq_bp.get('/search')
def buscar_faq():
    """Buscar preguntas frecuentes por palabra clave"""
    try:
        palabra_clave = request.args.get('q', '')
        if not palabra_clave:
            return jsonify({'error': 'Parámetro de búsqueda requerido'}), 400
        
        faqs = buscar_faq_use_case.ejecutar(palabra_clave)
        
        # Convertir entidades a diccionarios para JSON
        faqs_data = []
        for faq in faqs:
            faqs_data.append({
                'id': faq.id,
                'pregunta': faq.pregunta,
                'respuesta': faq.respuesta
            })
        
        return jsonify(faqs_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500








