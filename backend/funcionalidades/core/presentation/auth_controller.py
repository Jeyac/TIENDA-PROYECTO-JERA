from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import os

from funcionalidades.core.infraestructura.auth import generate_token, jwt_required
from funcionalidades.core.infraestructura.security import hash_password, verify_password
from funcionalidades.core.infraestructura.database import db
from funcionalidades.usuarios.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from funcionalidades.usuarios.application.use_cases.autenticar_usuario_use_case import AutenticarUsuarioUseCase
from funcionalidades.usuarios.infrastructure.usuario_repository_impl import UsuarioRepositoryImpl
from funcionalidades.core.exceptions.auth_exceptions import InvalidCredentialsError, AuthorizationError
from funcionalidades.core.exceptions import NotFoundError, BadRequestError

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
        print(f"\n=== DEBUG LOGIN ===")
        print(f"Datos recibidos: {data}")
        
        # Aceptar tanto 'username' como 'username_or_email'
        username_or_email = data.get('username') or data.get('username_or_email')
        password = data.get('password')
        
        print(f"username_or_email: {username_or_email}")
        print(f"password recibida: {'***' if password else None}")
        
        if not data or not username_or_email or not password:
            print("ERROR: Faltan credenciales")
            return jsonify({'error': 'Username/email y password son requeridos'}), 400
        
        # Autenticar usuario
        print("Intentando autenticar usuario...")
        usuario = autenticar_usuario_use_case.ejecutar(username_or_email, password)
        print(f"Usuario autenticado exitosamente: ID={usuario.id}, username={usuario.username}, rol={usuario.rol}")
        
        if not usuario:
            print("ERROR: Usuario no encontrado después de autenticar")
            raise InvalidCredentialsError("Credenciales inválidas")
        
        # Generar tokens
        print("Generando tokens...")
        access_token = generate_token(
            user_id=usuario.id,
            username=usuario.username,
            rol=usuario.rol,
            expires_minutes=int(os.getenv('JWT_EXPIRES_MINUTES'))
        )
        
        refresh_token = generate_token(
            user_id=usuario.id,
            username=usuario.username,
            rol=usuario.rol,
            expires_minutes=int(os.getenv('JWT_REFRESH_EXPIRES_MINUTES'))
        )
        
        print("Tokens generados exitosamente")
        print(f"=== FIN DEBUG LOGIN ===\n")
        
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
        print(f"ERROR: Credenciales inválidas - {str(e)}")
        return jsonify({'error': str(e)}), 401
    except (NotFoundError, BadRequestError) as e:
        print(f"ERROR: Not Found o Bad Request - {str(e)}")
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        print(f"\n!!! ERROR CRÍTICO EN LOGIN !!!")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"!!! FIN ERROR CRÍTICO !!!\n")
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
            expires_minutes=int(os.getenv('JWT_EXPIRES_MINUTES'))
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


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Solicitar restablecimiento de contraseña"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email requerido'}), 400
        
        email = data['email']
        
        # Verificar si el usuario existe
        from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
        from funcionalidades.auth.infrastructure.password_reset_model import PasswordResetModel
        from funcionalidades.auth.infrastructure.email_service import EmailService
        
        usuario = UsuarioModel.query.filter_by(email=email).first()
        
        if not usuario:
            # Por seguridad, devolver el mismo mensaje aunque el usuario no exista
            return jsonify({
                'message': f'Si el email {email} está registrado, recibirás un enlace de recuperación.'
            }), 200
        
        # Crear token de reset
        reset_token = PasswordResetModel.create_reset_token(usuario.id)
        
        # Enviar email
        email_service = EmailService()
        email_sent = email_service.send_password_reset_email(
            to_email=usuario.email,
            username=usuario.username,
            reset_token=reset_token.token
        )
        
        if email_sent:
            return jsonify({
                'message': f'Se ha enviado un enlace de recuperación a {email}. Revisa tu bandeja de entrada.'
            }), 200
        else:
            return jsonify({
                'message': f'Error enviando el email. Intenta de nuevo más tarde.'
            }), 500
        
    except Exception as e:
        print(f"Error en reset-password: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/reset-password/validate', methods=['POST'])
def validate_reset_token():
    """Validar token de reset de contraseña"""
    try:
        data = request.get_json()
        
        if not data or not data.get('token'):
            return jsonify({'error': 'Token requerido'}), 400
        
        token = data['token']
        
        # Validar token
        from funcionalidades.auth.infrastructure.password_reset_model import PasswordResetModel
        reset_token = PasswordResetModel.validate_token(token)
        
        if not reset_token:
            return jsonify({'error': 'Token inválido o expirado'}), 400
        
        return jsonify({
            'valid': True,
            'user_id': reset_token.user_id,
            'username': reset_token.user.username
        }), 200
        
    except Exception as e:
        print(f"Error validando token: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@auth_bp.route('/reset-password/confirm', methods=['POST'])
def confirm_password_reset():
    """Confirmar cambio de contraseña con token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('token') or not data.get('new_password'):
            return jsonify({'error': 'Token y nueva contraseña requeridos'}), 400
        
        token = data['token']
        new_password = data['new_password']
        
        if len(new_password) < 8:
            return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400
        
        # Validar token
        from funcionalidades.auth.infrastructure.password_reset_model import PasswordResetModel
        from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
        from funcionalidades.core.infraestructura.security import hash_password
        
        reset_token = PasswordResetModel.validate_token(token)
        
        if not reset_token:
            return jsonify({'error': 'Token inválido o expirado'}), 400
        
        # Cambiar contraseña
        usuario = UsuarioModel.query.get(reset_token.user_id)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        usuario.password_hash = hash_password(new_password)
        
        # Marcar token como usado
        reset_token.mark_as_used()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Contraseña actualizada exitosamente'
        }), 200
        
    except Exception as e:
        print(f"Error confirmando reset: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error interno del servidor'}), 500
