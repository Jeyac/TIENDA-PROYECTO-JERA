#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['*'], supports_credentials=True)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.route('/api/test-cors', methods=['GET', 'OPTIONS'])
def test_cors():
    return jsonify({'message': 'CORS funcionando correctamente'})

@app.route('/api/admin/chats', methods=['GET', 'OPTIONS'])
def get_chats():
    return jsonify([
        {
            'id': 1,
            'usuario_id': 1,
            'mensaje': 'Hola, necesito ayuda con mi pedido',
            'timestamp': '2025-10-03T10:30:00Z',
            'tipo': 'usuario'
        },
        {
            'id': 2,
            'usuario_id': 1,
            'mensaje': 'Hola! ¿En qué puedo ayudarte?',
            'timestamp': '2025-10-03T10:31:00Z',
            'tipo': 'bot'
        }
    ])

@app.route('/api/admin/kpis', methods=['GET', 'OPTIONS'])
def kpis():
    return jsonify({
        'usuarios_total': 10,
        'productos_total': 25,
        'ingresos_total': 1500.50
    })

@app.route('/api/admin/pedidos', methods=['GET', 'OPTIONS'])
def get_pedidos():
    return jsonify([
        {
            'id': 1,
            'usuario_id': 1,
            'total': 150.00,
            'created_at': '2025-10-03T10:30:00Z',
            'datos_facturacion': {'nombre': 'Juan Pérez'},
            'items': []
        }
    ])

@app.route('/api/admin/rag/files', methods=['GET', 'OPTIONS'])
def get_rag_files():
    return jsonify([
        {
            'id': 1,
            'nombre': 'manual_usuario.pdf',
            'tamaño': '2.5 MB',
            'fecha_subida': '2025-10-03T10:00:00Z'
        }
    ])

if __name__ == '__main__':
    print("Starting simple backend server...")
    app.run(host='0.0.0.0', port=5000, debug=True)




















