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


