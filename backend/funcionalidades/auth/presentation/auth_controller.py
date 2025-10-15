from flask import Blueprint, request, jsonify
from funcionalidades.core.infraestructura.auth import jwt_required
from funcionalidades.core.infraestructura.database import db
from funcionalidades.auth.application.use_cases.crear_token_reset_password_use_case import CrearTokenResetPasswordUseCase
from funcionalidades.auth.application.use_cases.validar_token_reset_password_use_case import ValidarTokenResetPasswordUseCase
from funcionalidades.auth.application.use_cases.usar_token_reset_password_use_case import UsarTokenResetPasswordUseCase
from funcionalidades.auth.application.use_cases.enviar_email_reset_password_use_case import EnviarEmailResetPasswordUseCase
from funcionalidades.auth.infrastructure.password_reset_repository_impl import PasswordResetRepositoryImpl
from funcionalidades.auth.infrastructure.email_service import EmailService

auth_bp = Blueprint('auth', __name__)

# Inicializar casos de uso
password_reset_repository = PasswordResetRepositoryImpl()
email_service = EmailService()
crear_token_reset_password_use_case = CrearTokenResetPasswordUseCase(password_reset_repository)
validar_token_reset_password_use_case = ValidarTokenResetPasswordUseCase(password_reset_repository)
usar_token_reset_password_use_case = UsarTokenResetPasswordUseCase(password_reset_repository)
enviar_email_reset_password_use_case = EnviarEmailResetPasswordUseCase(email_service)


@auth_bp.route('/request-password-reset', methods=['POST', 'OPTIONS'])
def request_password_reset():
    """Solicitar reset de contraseña"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'error': 'Email requerido'}), 400
        
        email = data['email']
        
        # Buscar usuario por email
        from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
        user = UsuarioModel.query.filter_by(email=email).first()
        
        if not user:
            # Por seguridad, no revelar si el email existe o no
            return jsonify({'message': 'Si el email existe, se enviará un enlace de recuperación'}), 200
        
        # Crear token de reset
        password_reset = crear_token_reset_password_use_case.ejecutar(user.id)
        
        # Enviar email
        email_sent = enviar_email_reset_password_use_case.ejecutar(
            password_reset=password_reset,
            username=user.username,
            email=user.email
        )
        
        if email_sent:
            return jsonify({'message': 'Se ha enviado un enlace de recuperación a tu email'}), 200
        else:
            return jsonify({'error': 'Error al enviar el email'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/validate-reset-token', methods=['POST', 'OPTIONS'])
def validate_reset_token():
    """Validar token de reset de contraseña"""
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({'error': 'Token requerido'}), 400
        
        token = data['token']
        
        # Validar token
        password_reset = validar_token_reset_password_use_case.ejecutar(token)
        
        return jsonify({
            'valid': True,
            'user_id': password_reset.user_id,
            'expires_at': password_reset.expires_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/reset-password', methods=['POST', 'OPTIONS'])
def reset_password():
    """Resetear contraseña usando token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Datos requeridos'}), 400
        
        required_fields = ['token', 'new_password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        token = data['token']
        new_password = data['new_password']
        
        # Validar token
        password_reset = validar_token_reset_password_use_case.ejecutar(token)
        
        # Actualizar contraseña del usuario
        from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
        from funcionalidades.core.infraestructura.security import hash_password
        
        user = UsuarioModel.query.get(password_reset.user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        user.password_hash = hash_password(new_password)
        db.session.commit()
        
        # Marcar token como usado
        usar_token_reset_password_use_case.ejecutar(token)
        
        return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
