from funcionalidades.core.infraestructura.database import db


class ProductoModel(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagenes = db.Column(db.JSON, nullable=False, default=list)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)


