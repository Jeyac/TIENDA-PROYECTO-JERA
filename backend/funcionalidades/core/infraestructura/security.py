import base64
import hashlib
import hmac
import os
from typing import Tuple


def hash_password(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError('password inválida')
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return base64.b64encode(salt).decode('utf-8') + ':' + base64.b64encode(dk).decode('utf-8')


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_b64, dk_b64 = stored.split(':', 1)
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(dk_b64)
        candidate = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False






