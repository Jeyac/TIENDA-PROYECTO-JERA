from flask import Blueprint, jsonify, request

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
from funcionalidades.productos.infrastructure.producto_model import ProductoModel
from funcionalidades.pedidos.infrastructure.pedido_model import PedidoModel


admin_bp = Blueprint('admin', __name__)


@admin_bp.get('/kpis')
@jwt_required(roles={'administrador'})
def kpis():
    start = request.args.get('start')
    end = request.args.get('end')
    q = PedidoModel.query
    if start:
        q = q.filter(PedidoModel.created_at >= start)
    if end:
        q = q.filter(PedidoModel.created_at <= end)
    usuarios_total = UsuarioModel.query.count()
    productos_total = ProductoModel.query.count()
    ingresos_total = sum(p.total for p in q.all())
    return jsonify({
        'usuarios_total': usuarios_total,
        'productos_total': productos_total,
        'ingresos_total': ingresos_total
    })


@admin_bp.get('/pedidos')
@jwt_required(roles={'administrador'})
def get_pedidos():
    """Obtener todos los pedidos para el admin"""
    pedidos = PedidoModel.query.all()
    return jsonify([{
        'id': p.id,
        'usuario_id': p.usuario_id,
        'total': p.total,
        'created_at': p.created_at.isoformat() if p.created_at else None,
        'datos_facturacion': p.datos_facturacion,
        'items': [{
            'producto_id': item.producto_id,
            'cantidad': item.cantidad,
            'precio_unitario': item.precio_unitario
        } for item in p.items]
    } for p in pedidos])


