from flask import Blueprint, jsonify, request

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.core.exceptions import BadRequestError, NotFoundError
from funcionalidades.pedidos.application.use_cases.crear_pedido_use_case import CrearPedidoUseCase
from funcionalidades.pedidos.application.use_cases.listar_pedidos_use_case import ListarPedidoseSUseCase
from funcionalidades.pedidos.application.use_cases.obtener_pedido_use_case import ObtenerPedidoUseCase
from funcionalidades.pedidos.application.use_cases.actualizar_pedido_use_case import ActualizarPedidoUseCase
from funcionalidades.pedidos.application.use_cases.eliminar_pedido_use_case import EliminarPedidoUseCase
from funcionalidades.pedidos.domain.entities.pedido_entity import Pedido, PedidoItem
from funcionalidades.pedidos.domain.repositories.pedido_repository import PedidoRepository
from funcionalidades.pedidos.infrastructure.pedido_repository_impl import PedidoRepositoryImpl, _to_entity


pedidos_bp = Blueprint('pedidos', __name__)
repo: PedidoRepository = PedidoRepositoryImpl()


@pedidos_bp.post('/')
@jwt_required
def crear_pedido():
    data = request.get_json(silent=True) or {}
    usuario_id = data.get('usuario_id')
    items = data.get('items', [])
    datos_facturacion = data.get('datos_facturacion', {})
    try:
        pedido = CrearPedidoUseCase(repo).ejecutar(usuario_id, items, datos_facturacion)
        return jsonify({
            'id': pedido.id,
            'usuario_id': pedido.usuario_id,
            'total': pedido.total,
            'datos_facturacion': pedido.datos_facturacion,
            'items': [{'producto_id': i.producto_id, 'cantidad': i.cantidad, 'precio_unitario': i.precio_unitario} for i in pedido.items]
        }), 201
    except BadRequestError as exc:
        return jsonify({'message': str(exc)}), 400


@pedidos_bp.get('/')
@jwt_required
def listar_pedidos():
    # Admin ve todos, usuario solo los suyos
    from funcionalidades.core.infraestructura.auth import decode_token
    from funcionalidades.core.exceptions.auth_exceptions import AuthorizationError
    from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
    
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise AuthorizationError('Falta token Bearer')
    token = auth_header.split(' ', 1)[1]
    payload = decode_token(token)
    username = payload['username']  # Cambiado de 'sub' a 'username'
    user = UsuarioModel.query.filter_by(username=username).first()
    
    if user.rol == 'administrador':
        # Admin ve todos
        items = ListarPedidoseSUseCase(repo).ejecutar()
    else:
        # Usuario ve solo los suyos
        from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel
        pedidos = PedidoModel.query.filter_by(usuario_id=user.id).all()
        items = [_to_entity(p) for p in pedidos]
    
    result = [{
        'id': p.id,
        'usuario_id': p.usuario_id,
        'total': p.total,
        'estado': getattr(p, 'estado', 'pendiente'),
        'created_at': getattr(p, 'created_at', None),
        'datos_facturacion': p.datos_facturacion,
        'items': [{'producto_id': i.producto_id, 'cantidad': i.cantidad, 'precio_unitario': i.precio_unitario} for i in p.items]
    } for p in items]
    return jsonify(result)


@pedidos_bp.get('/mis')
@jwt_required
def mis_pedidos():
    """Endpoint específico para que los clientes vean sus propios pedidos"""
    try:
        from funcionalidades.core.infraestructura.auth import decode_token
        from funcionalidades.core.exceptions.auth_exceptions import AuthorizationError
        from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
        from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel
        
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise AuthorizationError('Falta token Bearer')
        
        token = auth_header.split(' ', 1)[1]
        payload = decode_token(token)
        username = payload['username']
        
        user = UsuarioModel.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'Usuario no encontrado'}), 404
        
        # Obtener pedidos del usuario
        pedidos = PedidoModel.query.filter_by(usuario_id=user.id).all()
        
        result = []
        for pedido in pedidos:
            # Información básica del pedido
            result.append({
                'id': pedido.id,
                'usuario_id': pedido.usuario_id,
                'total': pedido.total,
                'estado': getattr(pedido, 'estado', 'pendiente'),
                'fecha_creacion': pedido.created_at.isoformat() if hasattr(pedido, 'created_at') and pedido.created_at else None,
                'datos_facturacion': getattr(pedido, 'datos_facturacion', {}) or {},
                'items_count': len(pedido.items) if pedido.items else 0,
                'items_preview': f'Pedido {pedido.id}'
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error en mis_pedidos: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Error interno del servidor', 'error': str(e)}), 500


@pedidos_bp.get('/test')
@jwt_required
def test_pedidos():
    """Endpoint de prueba simple"""
    try:
        print("DEBUG: Endpoint de prueba iniciado")
        return jsonify({
            'message': 'Endpoint de prueba funcionando',
            'status': 'ok',
            'timestamp': '2024-01-01T00:00:00Z'
        })
    except Exception as e:
        print(f"Error en test_pedidos: {e}")
        return jsonify({'message': 'Error en endpoint de prueba', 'error': str(e)}), 500


@pedidos_bp.get('/<int:pedido_id>')
@jwt_required
def obtener_pedido(pedido_id: int):
    try:
        from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel
        from funcionalidades.productos.infrastructure.producto_model import ProductoModel
        
        # Usar directamente el modelo en lugar del use case
        pedido = PedidoModel.query.get(pedido_id)
        if not pedido:
            return jsonify({'message': 'Pedido no encontrado'}), 404
        
        # Obtener información de productos para cada item
        items_with_products = []
        for item in pedido.items:
            try:
                producto = ProductoModel.query.filter_by(id=item.producto_id).first()
                items_with_products.append({
                    'id': item.id,
                    'producto_id': item.producto_id,
                    'cantidad': item.cantidad,
                    'precio_unitario': item.precio_unitario,
                    'precio': item.precio_unitario,
                    'producto_titulo': producto.titulo if producto else f'Producto {item.producto_id}',
                    'producto_descripcion': producto.descripcion if producto else 'Sin descripción'
                })
            except Exception:
                items_with_products.append({
                    'id': item.id,
                    'producto_id': item.producto_id,
                    'cantidad': item.cantidad,
                    'precio_unitario': item.precio_unitario,
                    'precio': item.precio_unitario,
                    'producto_titulo': f'Producto {item.producto_id}',
                    'producto_descripcion': 'Sin descripción'
                })
        
        return jsonify({
            'id': pedido.id,
            'usuario_id': pedido.usuario_id,
            'total': pedido.total,
            'datos_facturacion': pedido.datos_facturacion,
            'items': items_with_products
        })
    except Exception as e:
        print(f"Error en obtener_pedido: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Error interno del servidor', 'error': str(e)}), 500


@pedidos_bp.put('/<int:pedido_id>')
@jwt_required
def actualizar_pedido(pedido_id: int):
    data = request.get_json(silent=True) or {}
    items = data.get('items', [])
    try:
        p = ActualizarPedidoUseCase(repo).ejecutar(pedido_id, items)
        return jsonify({
            'id': p.id,
            'usuario_id': p.usuario_id,
            'total': p.total,
            'datos_facturacion': p.datos_facturacion,
            'items': [{'producto_id': i.producto_id, 'cantidad': i.cantidad, 'precio_unitario': i.precio_unitario} for i in p.items]
        })
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404


@pedidos_bp.delete('/<int:pedido_id>')
@jwt_required
def eliminar_pedido(pedido_id: int):
    try:
        EliminarPedidoUseCase(repo).ejecutar(pedido_id)
        return jsonify({'message': 'Eliminado'})
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404


@pedidos_bp.put('/<int:pedido_id>/cancelar')
@jwt_required(roles={'administrador'})
def cancelar_pedido(pedido_id: int):
    """Cancelar un pedido (solo administradores)"""
    try:
        from funcionalidades.pedidos.application.use_cases.actualizar_estado_pedido_use_case import ActualizarEstadoPedidoUseCase
        
        # Verificar que el pedido existe
        pedido = repo.get_by_id(pedido_id)
        if not pedido:
            return jsonify({'message': 'Pedido no encontrado'}), 404
        
        # Verificar que el pedido se puede cancelar
        from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel
        pedido_model = PedidoModel.query.get(pedido_id)
        if pedido_model.estado == 'entregado':
            return jsonify({'message': 'No se puede cancelar un pedido ya entregado'}), 400
        if pedido_model.estado == 'cancelado':
            return jsonify({'message': 'El pedido ya está cancelado'}), 400
        
        # Cancelar el pedido usando el caso de uso
        use_case = ActualizarEstadoPedidoUseCase(repo)
        use_case.ejecutar(pedido_id, 'cancelado')
        
        return jsonify({'message': 'Pedido cancelado exitosamente'})
        
    except Exception as e:
        return jsonify({'message': f'Error interno del servidor: {str(e)}'}), 500


