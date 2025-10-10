from flask import Blueprint, jsonify, request

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.core.infraestructura.database import db
from sqlalchemy import func
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
from funcionalidades.productos.infrastructure.producto_model import ProductoModel
from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel
from funcionalidades.chatlog.infrastructure.chat_message_model import ChatMessageModel
from funcionalidades.rag.infrastructure.documento_model import DocumentoModel, DocumentoChunkModel
from funcionalidades.rag.infrastructure.embedder_openai import OpenAIEmbedder
from funcionalidades.categorias.infrastructure.categoria_model import CategoriaModel


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/kpis', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def kpis():
    try:
        print("=== Calculando KPIs ===")

        usuarios_total = db.session.query(func.count(UsuarioModel.id)).scalar() or 0
        productos_total = db.session.query(func.count(ProductoModel.id)).filter(ProductoModel.activo == True).scalar() or 0
        ingresos_total = db.session.query(func.coalesce(func.sum(PedidoModel.total), 0)).scalar() or 0
        
        kpis_data = {
            'usuarios_total': usuarios_total,
            'productos_total': productos_total,
            'ingresos_total': ingresos_total
        }
        
        print(f"KPIs calculados: {kpis_data}")
        return jsonify(kpis_data)
        
    except Exception as e:
        # Fallback seguro para no romper el dashboard (pero conservar log en consola)
        print(f"Error calculando KPIs: {e}")
        return jsonify({
            'usuarios_total': 0,
            'productos_total': 0,
            'ingresos_total': 0
        })


@admin_bp.route('/pedidos', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_pedidos():
    """Obtener todos los pedidos para el admin con información del usuario."""
    try:
        # Join con usuarios para obtener información del usuario
        from funcionalidades.productos.infrastructure.producto_model import ProductoModel
        pedidos = db.session.query(PedidoModel, UsuarioModel).join(
            UsuarioModel, PedidoModel.usuario_id == UsuarioModel.id
        ).order_by(PedidoModel.created_at.desc()).all()
        
        response = []
        for pedido, usuario in pedidos:
            try:
                # Calcular cantidad total de productos
                productos_count = sum(item.cantidad for item in pedido.items) if pedido.items else 0
                
                # Obtener información de productos de manera más eficiente
                productos_info = []
                for item in pedido.items:
                    try:
                        # Usar filter_by en lugar de get para mejor compatibilidad
                        producto = ProductoModel.query.filter_by(id=item.producto_id).first()
                        print(f"DEBUG: Buscando producto ID {item.producto_id}")
                        print(f"DEBUG: Producto encontrado: {producto}")
                        if producto:
                            print(f"DEBUG: Título del producto: {producto.titulo}")
                        
                        productos_info.append({
                            'id': item.id,
                            'producto_id': item.producto_id,
                            'cantidad': item.cantidad,
                            'precio_unitario': item.precio_unitario,
                            'titulo': producto.titulo if producto else f'Producto {item.producto_id}',
                            'descripcion': producto.descripcion if producto else '',
                            'precio': item.precio_unitario
                        })
                    except Exception as e:
                        print(f"ERROR obteniendo producto {item.producto_id}: {e}")
                        import traceback
                        traceback.print_exc()
                        productos_info.append({
                            'id': item.id,
                            'producto_id': item.producto_id,
                            'cantidad': item.cantidad,
                            'precio_unitario': item.precio_unitario,
                            'titulo': f'Producto {item.producto_id}',
                            'descripcion': '',
                            'precio': item.precio_unitario
                        })
                
                response.append({
                    'id': pedido.id,
                    'usuario_id': pedido.usuario_id,
                    'usuario_nombre': usuario.username,
                    'usuario_email': usuario.email,
                    'total': pedido.total or 0,
                    'estado': pedido.estado or 'pendiente',
                    'fecha_creacion': pedido.created_at.isoformat() if pedido.created_at else None,
                    'datos_facturacion': pedido.datos_facturacion or {},
                    'productos_count': productos_count,
                    'productos': productos_info
                })
            except Exception as inner_e:
                print(f"Pedido inválido omitido: {inner_e}")
                import traceback
                traceback.print_exc()
        
        return jsonify(response)
    except Exception as e:
        print(f"Error listando pedidos: {e}")
        return jsonify([])


@admin_bp.route('/chats', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_chats():
    """Obtener historial de chats reales de usuarios registrados"""
    try:
        # Obtener TODOS los mensajes de chat con LEFT JOIN para incluir mensajes sin usuario
        chats = db.session.query(ChatMessageModel, UsuarioModel).outerjoin(
            UsuarioModel, ChatMessageModel.user_id == UsuarioModel.id
        ).order_by(ChatMessageModel.created_at.asc()).all()  # Ordenar ascendente para mantener orden cronológico
        
        # Agrupar mensajes por conversación (usuario_id o sesión)
        conversations = {}
        for chat, usuario in chats:
            # Usar user_id como clave, o 'anonimo' si es None
            conv_key = chat.user_id if chat.user_id else 'anonimo'
            
            if conv_key not in conversations:
                conversations[conv_key] = {
                    'id': conv_key,
                    'usuario_id': chat.user_id,
                    'usuario_nombre': usuario.username if usuario else 'Usuario Anónimo',
                    'usuario_email': usuario.email if usuario else 'Sin email',
                    'mensajes': [],
                    'mensajes_count': 0,
                    'fecha_creacion': chat.created_at.isoformat() if chat.created_at else None,
                    'ultima_actividad': chat.created_at.isoformat() if chat.created_at else None
                }
            
            conversations[conv_key]['mensajes'].append({
                'id': chat.id,
                'contenido': chat.content,
                'tipo': 'usuario' if chat.role == 'user' else 'bot' if chat.role == 'assistant' else 'sistema',
                'fecha_creacion': chat.created_at.isoformat() if chat.created_at else None
            })
            conversations[conv_key]['mensajes_count'] += 1
            
            # Actualizar última actividad
            if chat.created_at:
                current_ultima_actividad = conversations[conv_key]['ultima_actividad']
                chat_iso = chat.created_at.isoformat()
                if not current_ultima_actividad or chat_iso > current_ultima_actividad:
                    conversations[conv_key]['ultima_actividad'] = chat_iso
        
        # Convertir a lista y ordenar por última actividad (más reciente primero)
        response = list(conversations.values())
        response.sort(key=lambda x: x['ultima_actividad'] or '', reverse=True)
        
        print(f"DEBUG: Devolviendo {len(response)} conversaciones con {sum(c['mensajes_count'] for c in response)} mensajes totales")
        
        return jsonify(response)
    except Exception as e:
        print(f"Error listando chats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify([])


@admin_bp.route('/chats/<chat_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def delete_chat(chat_id):
    """Eliminar un chat específico o conversación completa"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        print(f"DEBUG: Eliminando chat/conversación: {chat_id}")
        
        if chat_id == 'anonimo':
            # Eliminar todos los mensajes sin usuario_id
            deleted_count = ChatMessageModel.query.filter_by(user_id=None).delete()
            db.session.commit()
            print(f"DEBUG: Eliminados {deleted_count} mensajes anónimos")
        else:
            # Eliminar mensajes de un usuario específico
            try:
                user_id = int(chat_id)
                deleted_count = ChatMessageModel.query.filter_by(user_id=user_id).delete()
                db.session.commit()
                print(f"DEBUG: Eliminados {deleted_count} mensajes del usuario {user_id}")
            except ValueError:
                return jsonify({'error': 'ID de chat inválido'}), 400
        
        return jsonify({'message': f'Chat eliminado correctamente. {deleted_count} mensajes eliminados.'})
    except Exception as e:
        print(f"Error eliminando chat: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/chats/clear', methods=['DELETE', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def clear_all_chats():
    """Eliminar todos los chats de la base de datos"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        print("DEBUG: Limpiando todos los chats...")
        
        # Eliminar todos los mensajes de chat
        deleted_count = ChatMessageModel.query.delete()
        db.session.commit()
        
        print(f"DEBUG: Eliminados {deleted_count} mensajes de chat")
        
        return jsonify({
            'message': f'Todos los chats han sido eliminados correctamente. {deleted_count} mensajes eliminados.'
        })
    except Exception as e:
        print(f"Error limpiando chats: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/rag/files', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_rag_files():
    """Listar documentos RAG desde base de datos para el admin."""
    try:
        docs = DocumentoModel.query.order_by(DocumentoModel.id.desc()).all()
        items = []
        for d in docs:
            try:
                # Inferir tipo por extensión si existe en el título
                nombre = d.titulo or ''
                partes = nombre.rsplit('.', 1)
                tipo = partes[1].lower() if len(partes) == 2 else 'txt'
                
                # Calcular tamaño del contenido en bytes
                contenido_bytes = len((d.contenido or '').encode('utf-8'))
                tamaño_mb = round(contenido_bytes / (1024 * 1024), 2)
                tamaño_str = f"{tamaño_mb} MB" if tamaño_mb >= 1 else f"{round(contenido_bytes / 1024, 1)} KB"
                
                items.append({
                    'id': d.id,
                    'nombre': nombre,
                    'tipo': tipo,
                    'tamaño': tamaño_str,
                    'descripcion': d.descripcion or '',
                    'fecha_subida': d.created_at.isoformat() if hasattr(d, 'created_at') and d.created_at else None
                })
            except Exception as inner_e:
                print(f"Documento inválido omitido: {inner_e}")
        return jsonify(items)
    except Exception as e:
        print(f"Error listando documentos RAG: {e}")
        return jsonify([])


@admin_bp.route('/rag/files/<int:file_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def delete_rag_file(file_id: int):
    """Eliminar un documento RAG por id (incluye chunks en cascada)."""
    try:
        doc = DocumentoModel.query.get(file_id)
        if not doc:
            return jsonify({'message': 'No encontrado'}), 404
        db.session.delete(doc)
        db.session.commit()
        return jsonify({'message': 'Documento eliminado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/rag/files/<int:file_id>', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_rag_file_detail(file_id: int):
    """Obtener detalle del documento (incluye contenido)."""
    try:
        doc = DocumentoModel.query.get(file_id)
        if not doc:
            return jsonify({'message': 'No encontrado'}), 404
        return jsonify({
            'id': doc.id,
            'nombre': doc.titulo,
            'contenido': doc.contenido
        })
    except Exception as e:
        print(f"Error obteniendo documento RAG: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/rag/files/<int:file_id>/chunks', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def get_rag_file_chunks(file_id: int):
    """Listar chunks del documento para inspección."""
    try:
        chunks = DocumentoChunkModel.query.filter_by(documento_id=file_id).order_by(DocumentoChunkModel.id.asc()).all()
        return jsonify([
            {
                'id': c.id,
                'texto': c.texto,
                'len': len(c.texto)
            } for c in chunks
        ])
    except Exception as e:
        print(f"Error listando chunks RAG: {e}")
        return jsonify([])


@admin_bp.route('/rag/process/<int:file_id>', methods=['POST', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def reprocess_rag_file(file_id: int):
    """Reprocesar documento: recalcular embeddings desde su contenido actual."""
    try:
        doc = DocumentoModel.query.get(file_id)
        if not doc:
            return jsonify({'message': 'No encontrado'}), 404

        # Borrar chunks existentes
        DocumentoChunkModel.query.filter_by(documento_id=file_id).delete()
        db.session.commit()

        # Re-crear chunks y embeddings
        def chunk_text(texto: str, max_len: int = 500):
            t = (texto or '').strip()
            while t:
                yield t[:max_len]
                t = t[max_len:]

        embedder = OpenAIEmbedder()
        for ch in chunk_text(doc.contenido):
            vector = embedder.embed(ch)
            db.session.add(DocumentoChunkModel(documento_id=file_id, texto=ch, embedding=vector))
        db.session.commit()

        return jsonify({'message': 'Documento reprocesado correctamente'})
    except Exception as e:
        db.session.rollback()
        print(f"Error reprocesando documento RAG: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/rag/files/<int:file_id>/download', methods=['GET', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def download_rag_file(file_id: int):
    """Descargar archivo RAG como archivo de texto."""
    try:
        doc = DocumentoModel.query.get(file_id)
        if not doc:
            return jsonify({'message': 'No encontrado'}), 404
        
        from flask import Response
        return Response(
            doc.contenido,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment; filename="{doc.titulo}"'
            }
        )
    except Exception as e:
        print(f"Error descargando documento RAG: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/pedidos/<int:pedido_id>', methods=['PUT', 'OPTIONS'])
@jwt_required(roles={'administrador'})
def update_pedido(pedido_id):
    """Actualizar estado de pedido"""
    try:
        print(f"DEBUG: Actualizando pedido {pedido_id}")
        pedido = PedidoModel.query.get_or_404(pedido_id)
        print(f"DEBUG: Pedido encontrado: {pedido.id}")
        
        data = request.get_json()
        print(f"DEBUG: Datos recibidos: {data}")
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        if 'estado' in data:
            print(f"DEBUG: Actualizando estado de {pedido.estado} a {data['estado']}")
            pedido.estado = data['estado']
        
        print(f"DEBUG: Guardando cambios...")
        db.session.commit()
        print(f"DEBUG: Cambios guardados exitosamente")
        
        return jsonify({
            'message': 'Pedido actualizado correctamente',
            'pedido': {
                'id': pedido.id,
                'estado': pedido.estado,
                'total': pedido.total
            }
        })
    except Exception as e:
        print(f"Error actualizando pedido: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500




