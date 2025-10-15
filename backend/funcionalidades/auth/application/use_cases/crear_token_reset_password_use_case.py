import secrets
import string
from datetime import datetime, timedelta
from funcionalidades.auth.domain.entities.password_reset_entity import PasswordReset
from funcionalidades.auth.domain.repositories.password_reset_repository import PasswordResetRepository
from funcionalidades.core.exceptions import BadRequestError


class CrearTokenResetPasswordUseCase:
    def __init__(self, password_reset_repo: PasswordResetRepository):
        self.password_reset_repo = password_reset_repo

    def ejecutar(self, user_id: int, expires_hours: int = 24) -> PasswordReset:
        """Crear token de reset de contraseña para un usuario"""
        if not user_id:
            raise BadRequestError('El ID del usuario es obligatorio')
        
        if expires_hours <= 0:
            raise BadRequestError('Las horas de expiración deben ser mayores a 0')
        
        # Invalidar tokens anteriores del usuario
        self.password_reset_repo.invalidar_tokens_usuario(user_id)
        
        # Generar token seguro
        token = self._generate_secure_token()
        
        # Calcular fecha de expiración
        expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
        
        # Crear entidad del dominio
        password_reset = PasswordReset(
            id=None,
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            used=False,
            created_at=None
        )
        
        return self.password_reset_repo.agregar(password_reset)

    def _generate_secure_token(self) -> str:
        """Generar token seguro para reset de contraseña"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
