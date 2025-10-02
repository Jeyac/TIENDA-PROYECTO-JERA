from flask import Blueprint, jsonify

from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel


usuarios_admin_bp = Blueprint('usuarios_admin', __name__)


@usuarios_admin_bp.get('/')
@jwt_required(roles={'administrador'})
def listar_usuarios():
    items = UsuarioModel.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email, 'rol': u.rol}
        for u in items
    ])


