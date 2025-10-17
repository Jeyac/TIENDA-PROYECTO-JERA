import os
from urllib.parse import urlparse

def get_database_url():
    """Construir la URL de la base de datos desde variables individuales"""
    # Si existe DATABASE_URL, usarla directamente
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # Si no, construir desde variables individuales
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    
    return f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require'

def get_cors_origins():
    """Obtener los orígenes permitidos para CORS"""
    cors_origins = os.getenv('CORS_ORIGINS', os.getenv('FRONTEND_URL', 'http://localhost:3000'))
    return cors_origins.split(',')

def get_jwt_secret():
    """Obtener la clave secreta para JWT"""
    return os.getenv('JWT_SECRET', os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production'))

def get_openai_key():
    """Obtener la clave de OpenAI"""
    return os.getenv('OPENAI_API_KEY', '')

def get_smtp_config():
    """Obtener configuración de SMTP"""
    return {
        'SMTP_SERVER': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'SMTP_PORT': int(os.getenv('SMTP_PORT', '587')),
        'SMTP_USERNAME': os.getenv('SMTP_USERNAME', ''),
        'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD', ''),
        'FROM_EMAIL': os.getenv('FROM_EMAIL', '')
    }

# Configuración para producción
PRODUCTION_CONFIG = {
    'DATABASE_URI': get_database_url(),
    'JWT_SECRET_KEY': get_jwt_secret(),
    'OPENAI_API_KEY': get_openai_key(),
    'CORS_ORIGINS': get_cors_origins(),
    'FLASK_ENV': 'production',
    'DEBUG': False,
    'JWT_EXPIRES_MINUTES': int(os.getenv('JWT_EXPIRES_MINUTES')),
    'JWT_REFRESH_EXPIRES_MINUTES': int(os.getenv('JWT_REFRESH_EXPIRES_MINUTES')),
    **get_smtp_config()
}
