from flask import Blueprint, jsonify, request

from funcionalidades.core.infraestructura.auth import create_access_token, create_refresh_token, decode_token
from funcionalidades.core.exceptions.auth_exceptions import AuthenticationError, AuthorizationError
from funcionalidades.core.exceptions import BadRequestError, NotFoundError
from funcionalidades.usuarios.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from funcionalidades.usuarios.application.use_cases.autenticar_usuario_use_case import AutenticarUsuarioUseCase
from funcionalidades.usuarios.infrastructure.usuario_repository_impl import UsuarioRepositoryImpl
from funcionalidades.usuarios.application.use_cases.restablecer_password_use_case import RestablecerPasswordUseCase


auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/login')
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Credenciales inválidas'}), 400

    repo = UsuarioRepositoryImpl()
    try:
        user = AutenticarUsuarioUseCase(repo).ejecutar(username, password)
        access = create_access_token(subject=user.username, role=user.rol)
        refresh = create_refresh_token(subject=user.username)
        return jsonify({'access_token': access, 'refresh_token': refresh, 'rol': user.rol})
    except (BadRequestError, NotFoundError) as exc:
        return jsonify({'message': str(exc)}), 401


@auth_bp.post('/refresh')
def refresh():
    data = request.get_json(silent=True) or {}
    token = data.get('refresh_token')
    if not token:
        return jsonify({'message': 'Falta refresh_token'}), 400
    try:
        payload = decode_token(token)
        if payload.get('type') != 'refresh':
            return jsonify({'message': 'Token no es refresh'}), 401
        new_access = create_access_token(subject=payload['sub'])
        return jsonify({'access_token': new_access})
    except (AuthenticationError, AuthorizationError) as exc:
        return jsonify({'message': str(exc)}), 401


@auth_bp.post('/register')
def register():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    rol = data.get('rol', 'cliente')
    if not username or not email or not password:
        return jsonify({'message': 'Datos incompletos'}), 400
    repo = UsuarioRepositoryImpl()
    try:
        user = RegistrarUsuarioUseCase(repo).ejecutar(username, email, password, rol)
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'rol': user.rol}), 201
    except BadRequestError as exc:
        return jsonify({'message': str(exc)}), 400


@auth_bp.post('/reset_password')
def reset_password():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    new_password = data.get('new_password')
    if not username or not new_password:
        return jsonify({'message': 'Datos incompletos'}), 400
    repo = UsuarioRepositoryImpl()
    try:
        user = RestablecerPasswordUseCase(repo).ejecutar(username, new_password)
        return jsonify({'id': user.id, 'username': user.username})
    except (BadRequestError, NotFoundError) as exc:
        return jsonify({'message': str(exc)}), 400


