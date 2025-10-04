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
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({'error': 'Credenciales inválidas'}), 400

    repo = UsuarioRepositoryImpl()
    try:
        user = AutenticarUsuarioUseCase(repo).ejecutar(username_or_email, password)
        access = create_access_token(subject=user.username, role=user.rol)
        refresh = create_refresh_token(subject=user.username)
        return jsonify({
            'access_token': access, 
            'refresh_token': refresh, 
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rol': user.rol
            }
        })
    except (BadRequestError, NotFoundError) as exc:
        return jsonify({'error': str(exc)}), 401


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
    confirm_password = data.get('confirm_password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    if password != confirm_password:
        return jsonify({'error': 'Las contraseñas no coinciden'}), 400
    
    if len(password) < 8:
        return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400
    
    repo = UsuarioRepositoryImpl()
    try:
        user = RegistrarUsuarioUseCase(repo).ejecutar(username, email, password, 'cliente')
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rol': user.rol
            }
        }), 201
    except BadRequestError as exc:
        return jsonify({'error': str(exc)}), 400


@auth_bp.post('/reset-password')
def reset_password():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email requerido'}), 400
    
    # Por ahora solo simulamos el envío del correo
    # En producción aquí se enviaría un correo real con un enlace de reset
    return jsonify({
        'message': f'Se ha enviado un enlace de recuperación a {email}. Revisa tu bandeja de entrada.'
    }), 200


