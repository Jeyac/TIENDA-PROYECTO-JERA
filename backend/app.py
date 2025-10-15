import eventlet
eventlet.monkey_patch()

import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from funcionalidades.core.infraestructura.socketio import socketio

# Importar la instancia compartida de db
from funcionalidades.core.infraestructura.database import db
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    # Configurar CORS
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

    # Configuración básica
    from funcionalidades.core.infraestructura.config import load_settings
    settings = load_settings()

    app.config['SQLALCHEMY_DATABASE_URI'] = settings['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Deshabilitar redirecciones automáticas para evitar problemas con CORS
    app.url_map.strict_slashes = False
    
    # Configurar para servir archivos estáticos
    from flask import send_from_directory
    import os
    
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)

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
    from funcionalidades.analytics.presentation.analytics_controller import analytics_bp
    from funcionalidades.tickets.presentation.ticket_controller import ticket_bp
    from funcionalidades.productos.presentation.image_controller import image_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')
    app.register_blueprint(pedidos_bp, url_prefix='/api/pedidos')
    app.register_blueprint(rag_bp, url_prefix='/api/rag')
    app.register_blueprint(usuarios_admin_bp, url_prefix='/api/admin/usuarios')
    app.register_blueprint(chatlog_bp, url_prefix='/api/admin/chatlog')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(faq_bp, url_prefix='/api/faq')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(ticket_bp, url_prefix='/api/tickets')
    app.register_blueprint(image_bp, url_prefix='/api/images')

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

    @app.get('/admin/rag')
    def admin_rag_page():
        from flask import send_from_directory
        return send_from_directory('static', 'admin_rag.html')

    # Crear tablas y (opcional) seed inicial RAG si no hay documentos
    with app.app_context():
        db.create_all()
        # Controlar el seeding vía variable de entorno SEED_RAG=true
        if os.getenv('SEED_RAG', 'false').lower() == 'true':
            try:
                from funcionalidades.rag.infrastructure.documento_model import DocumentoModel  # noqa: F401
                if DocumentoModel.query.count() == 0:
                    from funcionalidades.rag.infrastructure.documento_repository_impl import DocumentoRepositoryImpl
                    from funcionalidades.rag.infrastructure.embedder_openai import OpenAIEmbedder
                    from funcionalidades.rag.application.use_cases.ingestar_documento_use_case import IngestarDocumentoUseCase

                    contenido_base = (
                        "Información de la tienda:\n"
                        "- Pedidos: Regístrate, añade productos al carrito y confirma el pago.\n"
                        "- Envíos: 2-5 días hábiles, seguimiento por correo.\n"
                        "- Devoluciones: 30 días, producto en buen estado con ticket.\n"
                        "- Soporte: rox17jacome@gmail.com, Lun-Vie 9:00-18:00.\n"
                    )
                    repo = DocumentoRepositoryImpl()
                    embedder = OpenAIEmbedder()
                    IngestarDocumentoUseCase(repo, embedder).ejecutar(
                        titulo="Guía de la tienda",
                        contenido=contenido_base,
                    )
            except Exception as e:
                # No interrumpir el arranque por fallo de seeding
                print(f"Warning: RAG seeding failed: {e}")

    return app


if __name__ == '__main__':
    application = create_app()
    # Registrar eventos de socket (import lado-efecto)
    from funcionalidades.core.presentation import chat_socket  # noqa: F401
    socketio.run(application, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


