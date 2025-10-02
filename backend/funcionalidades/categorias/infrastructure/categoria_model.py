from funcionalidades.core.infraestructura.database import db


class CategoriaModel(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    activa = db.Column(db.Boolean, nullable=False, default=True)