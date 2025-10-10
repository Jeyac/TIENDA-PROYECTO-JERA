from datetime import datetime, timezone, timedelta
from flask import current_app


def get_guatemala_time():
    """Obtener hora actual de Guatemala (UTC-6)"""
    # Zona horaria de Guatemala (UTC-6)
    guatemala_tz = timezone(timedelta(hours=-6))
    return datetime.now(guatemala_tz)


def get_guatemala_time_utc():
    """Obtener hora actual de Guatemala como datetime UTC"""
    guatemala_time = get_guatemala_time()
    return guatemala_time.replace(tzinfo=None)


def format_guatemala_time(date_obj=None, format_str='%Y-%m-%d %H:%M:%S'):
    """Formatear fecha/hora en zona horaria de Guatemala"""
    if date_obj is None:
        date_obj = get_guatemala_time()
    
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
    
    # Convertir a zona horaria de Guatemala
    guatemala_tz = timezone(timedelta(hours=-6))
    if date_obj.tzinfo is None:
        # Asumir que es UTC si no tiene zona horaria
        date_obj = date_obj.replace(tzinfo=timezone.utc)
    
    guatemala_time = date_obj.astimezone(guatemala_tz)
    return guatemala_time.strftime(format_str)



