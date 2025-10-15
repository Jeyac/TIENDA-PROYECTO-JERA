from typing import Optional
from datetime import datetime

from funcionalidades.core.infraestructura.database import db
from funcionalidades.auth.domain.entities.password_reset_entity import PasswordReset
from funcionalidades.auth.domain.repositories.password_reset_repository import PasswordResetRepository
from funcionalidades.auth.infrastructure.password_reset_model import PasswordResetModel


def _to_password_reset_entity(model: PasswordResetModel) -> PasswordReset:
    return PasswordReset(
        id=model.id,
        user_id=model.user_id,
        token=model.token,
        expires_at=model.expires_at,
        used=model.used,
        created_at=model.created_at
    )


def _to_password_reset_model(password_reset: PasswordReset) -> PasswordResetModel:
    return PasswordResetModel(
        id=password_reset.id,
        user_id=password_reset.user_id,
        token=password_reset.token,
        expires_at=password_reset.expires_at,
        used=password_reset.used,
        created_at=password_reset.created_at
    )


class PasswordResetRepositoryImpl(PasswordResetRepository):
    def agregar(self, password_reset: PasswordReset) -> PasswordReset:
        model = _to_password_reset_model(password_reset)
        db.session.add(model)
        db.session.commit()
        return _to_password_reset_entity(model)

    def get_by_token(self, token: str) -> Optional[PasswordReset]:
        model = PasswordResetModel.query.filter_by(token=token).first()
        return _to_password_reset_entity(model) if model else None

    def get_by_user_id(self, user_id: int) -> list[PasswordReset]:
        models = PasswordResetModel.query.filter_by(user_id=user_id).order_by(PasswordResetModel.created_at.desc()).all()
        return [_to_password_reset_entity(model) for model in models]

    def invalidar_tokens_usuario(self, user_id: int) -> None:
        PasswordResetModel.query.filter_by(user_id=user_id, used=False).update({'used': True})
        db.session.commit()

    def marcar_como_usado(self, token: str) -> None:
        model = PasswordResetModel.query.filter_by(token=token).first()
        if model:
            model.used = True
            db.session.commit()

    def eliminar_tokens_expirados(self) -> int:
        now = datetime.utcnow()
        expired_tokens = PasswordResetModel.query.filter(PasswordResetModel.expires_at < now).all()
        count = len(expired_tokens)
        
        for token in expired_tokens:
            db.session.delete(token)
        
        db.session.commit()
        return count
