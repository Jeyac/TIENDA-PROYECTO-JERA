from funcionalidades.core.infraestructura.database import db
from funcionalidades.core.infraestructura.timezone import get_guatemala_time_utc


class PedidoModel(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='pendiente')
    created_at = db.Column(db.DateTime, default=get_guatemala_time_utc, nullable=False)
    datos_facturacion = db.Column(db.JSON, nullable=False, default=dict)
    items = db.relationship('PedidoItemModel', backref='pedido', cascade='all, delete-orphan', lazy=True)


class PedidoItemModel(db.Model):
    __tablename__ = 'pedido_items'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)


