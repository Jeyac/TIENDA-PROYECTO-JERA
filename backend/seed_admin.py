#!/usr/bin/env python3
"""
Script para crear usuario administrador por defecto
"""
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from funcionalidades.core.infraestructura.database import db
from funcionalidades.core.infraestructura.security import hash_password
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel


def create_admin_user():
    """Crear usuario administrador por defecto"""
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existe un admin
        existing_admin = UsuarioModel.query.filter_by(rol='administrador').first()
        
        if existing_admin:
            print("✅ Ya existe un usuario administrador en el sistema")
            print(f"   Usuario: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            return
        
        # Crear usuario admin por defecto
        admin_data = {
            'username': 'admin',
            'email': 'admin@tienda.com',
            'password_hash': hash_password('372004'),
            'rol': 'administrador'
        }
        
        admin_user = UsuarioModel(**admin_data)
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente")
            print("   Usuario: admin")
            print("   Email: admin@tienda.com")
            print("   Contraseña: 372004")
            print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear usuario administrador: {e}")


if __name__ == '__main__':
    create_admin_user()
