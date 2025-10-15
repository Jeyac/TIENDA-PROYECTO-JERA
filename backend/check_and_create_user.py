"""Script para verificar y crear usuario admin si no existe"""
import os
import sys

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from funcionalidades.core.infraestructura.database import db
from funcionalidades.usuarios.infrastructure.usuario_model import UsuarioModel
from funcionalidades.core.infraestructura.security import hash_password

def main():
    app = create_app()
    
    with app.app_context():
        # Verificar usuarios existentes
        print("\n=== USUARIOS EN LA BASE DE DATOS ===")
        usuarios = UsuarioModel.query.all()
        
        if not usuarios:
            print("No hay usuarios en la base de datos.")
        else:
            print(f"Total de usuarios: {len(usuarios)}\n")
            for usuario in usuarios:
                print(f"ID: {usuario.id}")
                print(f"Username: {usuario.username}")
                print(f"Email: {usuario.email}")
                print(f"Rol: {usuario.rol}")
                print("-" * 40)
        
        # Preguntar si crear usuario
        print("\n¿Quieres crear un nuevo usuario? (s/n): ", end="")
        respuesta = input().strip().lower()
        
        if respuesta == 's':
            print("\n=== CREAR NUEVO USUARIO ===")
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            print("Rol (administrador/cliente) [cliente]: ", end="")
            rol = input().strip() or "cliente"
            
            # Verificar si ya existe
            existing = UsuarioModel.query.filter(
                (UsuarioModel.username == username) | (UsuarioModel.email == email)
            ).first()
            
            if existing:
                print(f"\n❌ ERROR: Ya existe un usuario con ese username o email")
                return
            
            # Crear usuario
            nuevo_usuario = UsuarioModel(
                username=username,
                email=email,
                password_hash=hash_password(password),
                rol=rol
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            print(f"\n✅ Usuario '{username}' creado exitosamente!")
            print(f"   Email: {email}")
            print(f"   Rol: {rol}")

if __name__ == '__main__':
    main()








