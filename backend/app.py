import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from funcionalidades.core.infraestructura.socketio import socketio

# Inicializaciones globales para ser importadas en otros módulos
db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    # Configuración básica
    from funcionalidades.core.infraestructura.config import load_settings
    settings = load_settings()

    app.config['SQLALCHEMY_DATABASE_URI'] = settings['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT (simple) - clave y expiraciones en minutos
    app.config['JWT_SECRET'] = settings['JWT_SECRET']
    app.config['JWT_EXPIRES_MINUTES'] = int(settings['JWT_EXPIRES_MINUTES'])
    app.config['JWT_REFRESH_EXPIRES_MINUTES'] = int(settings['JWT_REFRESH_EXPIRES_MINUTES'])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Registrar modelos para migraciones
    from funcionalidades.productos.infrastructure.producto_model import ProductoModel  # noqa: F401
    from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel  # noqa: F401
    from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel, PedidoItemModel  # noqa: F401
    from funcionalidades.rag.infrastructure.documento_model import DocumentoModel, DocumentoChunkModel  # noqa: F401
    from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel  # noqa: F401
    from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel  # noqa: F401

    # Blueprints
    from funcionalidades.productos.presentation.controllers.producto_controller import productos_bp
    from funcionalidades.pedidos.presentation.controllers.pedido_controller import pedidos_bp
    from funcionalidades.core.presentation.auth_controller import auth_bp
    from funcionalidades.rag.presentation.controllers import rag_bp
    from funcionalidades.usuarios.presentation.controllers import usuarios_admin_bp
    from funcionalidades.chatlog.presentation.controllers import chatlog_bp
    from funcionalidades.core.presentation.admin_controller import admin_bp
    from funcionalidades.faq.presentation.controllers import faq_bp
    from funcionalidades.categorias.presentation.controllers import categorias_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')
    app.register_blueprint(pedidos_bp, url_prefix='/api/pedidos')
    app.register_blueprint(rag_bp, url_prefix='/api/rag')
    app.register_blueprint(usuarios_admin_bp, url_prefix='/api/admin/usuarios')
    app.register_blueprint(chatlog_bp, url_prefix='/api/admin/chatlog')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(faq_bp, url_prefix='/api/faq')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')

    @app.get('/health')
    def health_check():
        return jsonify({
            'status': 'ok',
            'environment': settings['ENVIRONMENT']
        })

    @app.get('/chat')
    def chat_page():
        from flask import send_from_directory
        return send_from_directory('static', 'chat.html')

    return app


if __name__ == '__main__':
    application = create_app()
    # Registrar eventos de socket (import lado-efecto)
    from funcionalidades.core.presentation import chat_socket  # noqa: F401
    socketio.run(application, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


