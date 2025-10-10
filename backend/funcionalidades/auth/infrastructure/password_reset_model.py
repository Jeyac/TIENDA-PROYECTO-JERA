from datetime import datetime, timedelta
from funcionalidades.core.infraestructura.database import db
import secrets
import string

class PasswordResetModel(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relación con usuario
    user = db.relationship('UsuarioModel', backref='password_resets')

    @staticmethod
    def generate_token():
        """Generar token seguro para reset de contraseña"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

    @staticmethod
    def create_reset_token(user_id, expires_hours=24):
        """Crear token de reset para un usuario"""
        # Invalidar tokens anteriores del usuario
        PasswordResetModel.query.filter_by(user_id=user_id, used=False).update({'used': True})
        
        # Crear nuevo token
        token = PasswordResetModel.generate_token()
        expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
        
        reset_token = PasswordResetModel(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        
        db.session.add(reset_token)
        db.session.commit()
        
        return reset_token

    @staticmethod
    def validate_token(token):
        """Validar token de reset"""
        reset_token = PasswordResetModel.query.filter_by(
            token=token, 
            used=False
        ).first()
        
        if not reset_token:
            return None
            
        if reset_token.expires_at < datetime.utcnow():
            return None
            
        return reset_token

    def mark_as_used(self):
        """Marcar token como usado"""
        self.used = True
        db.session.commit()



