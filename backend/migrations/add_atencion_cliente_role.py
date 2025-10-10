"""
Script para agregar el rol de Atención al Cliente
Ejecutar con: python migrations/add_atencion_cliente_role.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from funcionalidades.core.infraestructura.database import db
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
from funcionalidades.core.infraestructura.config import load_settings
from funcionalidades.core.infraestructura.security import hash_password

def add_atencion_cliente_role():
    """Agregar usuario de ejemplo con rol atencion_cliente"""
    # Cargar configuración desde variables de entorno
    settings = load_settings()
    
    # Crear app Flask temporal
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            # Verificar si ya existe un usuario con este rol
            existing = UsuarioModel.query.filter_by(email='correodetrabajo12588@gmail.com').first()
            
            if existing:
                print("[OK] El usuario ya existe - Actualizando password...")
                # Actualizar el password con el hash correcto
                existing.password_hash = hash_password('372004')
                db.session.commit()
                print(f"   Username: {existing.username}")
                print(f"   Email: {existing.email}")
                print(f"   Rol: {existing.rol}")
                print("   Password actualizada correctamente")
                return
            
            print("Creando usuario de Atencion al Cliente...")
            
            # Crear usuario de ejemplo
            usuario = UsuarioModel(
                username='Roxana Jacome',
                email='correodetrabajo12588@gmail.com',
                password_hash=hash_password('372004'),
                rol='atencion_cliente',
                activo=True
            )
            
            db.session.add(usuario)
            db.session.commit()
            
            print("[OK] Usuario de Atencion al Cliente creado exitosamente!")
            print("   Username: Roxana Jacome")
            print("   Email: correodetrabajo12588@gmail.com")
            print("   Password: 372004")
            print("   Rol: atencion_cliente")
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_atencion_cliente_role()

