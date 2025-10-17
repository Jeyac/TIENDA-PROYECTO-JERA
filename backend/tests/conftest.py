import sys
import os
import pytest

# Agregar el directorio del proyecto al path de Python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture
def app():
    """Crear aplicación Flask para tests"""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        from funcionalidades.core.infraestructura.database import db
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de prueba para tests"""
    return app.test_client()
