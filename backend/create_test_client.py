#!/usr/bin/env python3
"""
Script para crear usuario cliente de prueba
"""
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from funcionalidades.core.infraestructura.database import db
from funcionalidades.core.infraestructura.security import hash_password
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel


def create_test_client():
    """Crear usuario cliente de prueba"""
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existe el usuario cliente de prueba
        existing_client = UsuarioModel.query.filter_by(username='cliente_test').first()
        
        if existing_client:
            print("✅ Ya existe el usuario cliente de prueba")
            print(f"   Usuario: {existing_client.username}")
            print(f"   Email: {existing_client.email}")
            return
        
        # Crear usuario cliente de prueba
        client_data = {
            'username': 'cliente_test',
            'email': 'cliente@test.com',
            'password_hash': hash_password('123456'),
            'rol': 'cliente',
            'activo': True
        }
        
        client_user = UsuarioModel(**client_data)
        
        try:
            db.session.add(client_user)
            db.session.commit()
            
            print("✅ Usuario cliente de prueba creado exitosamente")
            print("   Usuario: cliente_test")
            print("   Email: cliente@test.com")
            print("   Contraseña: 123456")
            print("   Rol: cliente")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear usuario cliente: {e}")


if __name__ == '__main__':
    create_test_client()




