from funcionalidades.core.infraestructura.database import db


class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(32), nullable=False, default='cliente')
    activo = db.Column(db.Boolean, nullable=False, default=True)


