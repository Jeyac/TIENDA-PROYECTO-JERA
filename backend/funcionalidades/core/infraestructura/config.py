import os
from typing import Dict

from dotenv import load_dotenv


def load_settings() -> Dict[str, str]:
    # Cargar variables desde .env si existe
    load_dotenv()

    environment = os.getenv('ENVIRONMENT', 'development')

    # Construcción de URI de base de datos
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')

    database_uri = ''
    if environment == 'production' and db_user and db_password and db_name:
        # Usar psycopg (SQLAlchemy 2 URL)
        database_uri = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        # Fallback a SQLite en desarrollo
        database_uri = os.getenv('DATABASE_URI', 'sqlite:///dev.db')

    settings = {
        'ENVIRONMENT': environment,
        'DATABASE_URI': database_uri,
        'JWT_SECRET': os.getenv('JWT_SECRET', 'change_me'),
        'JWT_EXPIRES_MINUTES': os.getenv('JWT_EXPIRES_MINUTES', '60'),
        'JWT_REFRESH_EXPIRES_MINUTES': os.getenv('JWT_REFRESH_EXPIRES_MINUTES', '10080'),
    }

    return settings


