import datetime as dt
from typing import Any, Dict, Iterable, Optional

import jwt
from flask import current_app, request
from functools import wraps

from funcionalidades.core.exceptions.auth_exceptions import AuthenticationError, AuthorizationError


def generate_token(user_id: int, username: str, rol: str, expires_minutes: int = 60) -> str:
    """Generar token JWT"""
    payload = {
        'user_id': user_id,
        'username': username,
        'rol': rol,
        'exp': dt.datetime.utcnow() + dt.timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def create_access_token(subject: str, role: Optional[str] = None) -> str:
    expires_minutes = int(current_app.config['JWT_EXPIRES_MINUTES'])
    payload = {
        'sub': subject,
        'type': 'access',
        'exp': dt.datetime.utcnow() + dt.timedelta(minutes=expires_minutes)
    }
    if role:
        payload['role'] = role
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def create_refresh_token(subject: str) -> str:
    expires_minutes = int(current_app.config['JWT_REFRESH_EXPIRES_MINUTES'])
    payload = {
        'sub': subject,
        'type': 'refresh',
        'exp': dt.datetime.utcnow() + dt.timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError as exc:
        raise AuthenticationError('Token expirado') from exc
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError('Token inválido') from exc


def jwt_required(fn=None, *, roles: Optional[Iterable[str]] = None):
    def decorator(inner_fn):
        @wraps(inner_fn)
        def wrapper(*args, **kwargs):
            # Permitir peticiones OPTIONS sin autenticación
            if request.method == 'OPTIONS':
                from flask import jsonify
                return jsonify({'status': 'ok'})
                
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                raise AuthorizationError('Falta token Bearer')
            token = auth_header.split(' ', 1)[1]
            payload = decode_token(token)
            
            # Verificar roles si se especifican
            if roles is not None:
                user_role = payload.get('rol')
                if user_role not in roles:
                    raise AuthorizationError('Rol no autorizado')
            
            # Agregar información del usuario al contexto de Flask
            from flask import g
            g.user_id = payload.get('user_id')
            g.username = payload.get('username')
            g.rol = payload.get('rol')
            
            return inner_fn(*args, **kwargs)
        return wrapper

    # Soporta @jwt_required y @jwt_required(...)
    if fn is not None and callable(fn):
        return decorator(fn)
    return decorator


def get_current_user_id() -> int:
    """Obtener el ID del usuario actual desde el contexto de Flask"""
    from flask import g
    if not hasattr(g, 'user_id'):
        raise AuthenticationError('No hay usuario autenticado')
    return g.user_id


def get_current_username() -> str:
    """Obtener el username del usuario actual desde el contexto de Flask"""
    from flask import g
    if not hasattr(g, 'username'):
        raise AuthenticationError('No hay usuario autenticado')
    return g.username


def get_current_user_role() -> str:
    """Obtener el rol del usuario actual desde el contexto de Flask"""
    from flask import g
    if not hasattr(g, 'rol'):
        raise AuthenticationError('No hay usuario autenticado')
    return g.rol


