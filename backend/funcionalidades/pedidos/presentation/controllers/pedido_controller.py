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
    username = payload['sub']
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
        'datos_facturacion': p.datos_facturacion,
        'items': [{'producto_id': i.producto_id, 'cantidad': i.cantidad, 'precio_unitario': i.precio_unitario} for i in p.items]
    } for p in items]
    return jsonify(result)


@pedidos_bp.get('/<int:pedido_id>')
@jwt_required
def obtener_pedido(pedido_id: int):
    try:
        p = ObtenerPedidoUseCase(repo).ejecutar(pedido_id)
        return jsonify({
            'id': p.id,
            'usuario_id': p.usuario_id,
            'total': p.total,
            'datos_facturacion': p.datos_facturacion,
            'items': [{'producto_id': i.producto_id, 'cantidad': i.cantidad, 'precio_unitario': i.precio_unitario} for i in p.items]
        })
    except NotFoundError as exc:
        return jsonify({'message': str(exc)}), 404


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


