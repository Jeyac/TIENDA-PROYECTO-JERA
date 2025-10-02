from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import os

from funcionalidades.core.infraestructura.auth import generate_token, jwt_required
from funcionalidades.core.infraestructura.security import hash_password, verify_password
from funcionalidades.usuarios.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from funcionalidades.usuarios.application.use_cases.autenticar_usuario_use_case import AutenticarUsuarioUseCase
from funcionalidades.usuarios.infrastructure.usuario_repository_impl import UsuarioRepositoryImpl
from funcionalidades.core.exceptions.auth_exceptions import InvalidCredentialsError, AuthorizationError

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Inicializar casos de uso
usuario_repository = UsuarioRepositoryImpl()
registrar_usuario_use_case = RegistrarUsuarioUseCase(usuario_repository)
autenticar_usuario_use_case = AutenticarUsuarioUseCase(usuario_repository)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registro de usuarios (solo clientes)"""
    try:
        data = request.get_json()
        
        # Validaciones básicas
        if not data:
            return jsonify({'error': 'Datos requeridos'}), 400
        
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        # Forzar rol de cliente (no permitir admin en registro)
        data['rol'] = 'cliente'
        
        # Registrar usuario
        usuario = registrar_usuario_use_case.ejecutar(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            rol=data['rol']
        )
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'rol': usuario.rol
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Inicio de sesión"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username y password son requeridos'}), 400
        
        # Autenticar usuario
        usuario = autenticar_usuario_use_case.ejecutar(
            username=data['username'],
            password=data['password']
        )
        
        if not usuario:
            raise InvalidCredentialsError("Credenciales inválidas")
        
        # Generar tokens
        access_token = generate_token(
            user_id=usuario.id,
            username=usuario.username,
            rol=usuario.rol,
            expires_minutes=int(os.getenv('JWT_EXPIRES_MINUTES', 60))
        )
        
        refresh_token = generate_token(
            user_id=usuario.id,
            username=usuario.username,
            rol=usuario.rol,
            expires_minutes=int(os.getenv('JWT_REFRESH_EXPIRES_MINUTES', 10080))
        )
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'rol': usuario.rol
            }
        }), 200
        
    except InvalidCredentialsError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Renovar access token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('refresh_token'):
            return jsonify({'error': 'Refresh token requerido'}), 400
        
        # Decodificar refresh token
        from funcionalidades.core.infraestructura.auth import decode_token
        payload = decode_token(data['refresh_token'])
        
        if not payload:
            return jsonify({'error': 'Token inválido'}), 401
        
        # Generar nuevo access token
        access_token = generate_token(
            user_id=payload['user_id'],
            username=payload['username'],
            rol=payload['rol'],
            expires_minutes=int(os.getenv('JWT_EXPIRES_MINUTES', 60))
        )
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtener información del usuario actual"""
    try:
        # El decorador jwt_required ya valida el token y pasa la info del usuario
        from flask import g
        return jsonify({
            'user': {
                'id': g.user_id,
                'username': g.username,
                'rol': g.rol
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500
