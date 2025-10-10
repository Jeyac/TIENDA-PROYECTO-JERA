import os
from typing import Dict, Any


def load_settings() -> Dict[str, Any]:
    """Cargar configuración de la aplicación desde variables de entorno"""
    
    # Cargar archivo .env si existe
    env_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    
    # Obtener entorno
    environment = os.getenv('FLASK_ENV', 'development')
    
    # Configuración de base de datos
    if environment == 'production':
        database_uri = os.getenv('DATABASE_URL', 'sqlite:///production.db')
    else:
        database_uri = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    
    # Configuración JWT
    jwt_secret = os.getenv('JWT_SECRET')
    if not jwt_secret:
        raise ValueError("JWT_SECRET no está definido en las variables de entorno")
    
    jwt_expires_minutes = os.getenv('JWT_EXPIRES_MINUTES')
    if not jwt_expires_minutes:
        raise ValueError("JWT_EXPIRES_MINUTES no está definido en las variables de entorno")
    jwt_expires_minutes = int(jwt_expires_minutes)
    
    jwt_refresh_expires_minutes = os.getenv('JWT_REFRESH_EXPIRES_MINUTES')
    if not jwt_refresh_expires_minutes:
        raise ValueError("JWT_REFRESH_EXPIRES_MINUTES no está definido en las variables de entorno")
    jwt_refresh_expires_minutes = int(jwt_refresh_expires_minutes)
    
    # Configuración SMTP
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    from_email = os.getenv('FROM_EMAIL', '')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # Configuración OpenAI
    openai_api_key = os.getenv('OPENAI_API_KEY', '')
    
    # Configuración de zona horaria
    timezone = os.getenv('TIMEZONE', 'America/Guatemala')
    
    settings = {
        'ENVIRONMENT': environment,
        'DATABASE_URI': database_uri,
        'JWT_SECRET': jwt_secret,
        'JWT_EXPIRES_MINUTES': jwt_expires_minutes,
        'JWT_REFRESH_EXPIRES_MINUTES': jwt_refresh_expires_minutes,
        'SMTP_SERVER': smtp_server,
        'SMTP_PORT': smtp_port,
        'SMTP_USERNAME': smtp_username,
        'SMTP_PASSWORD': smtp_password,
        'FROM_EMAIL': from_email,
        'FRONTEND_URL': frontend_url,
        'OPENAI_API_KEY': openai_api_key,
        'TIMEZONE': timezone
    }
    
    return settings