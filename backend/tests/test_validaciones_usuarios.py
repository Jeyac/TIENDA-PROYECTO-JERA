#!/usr/bin/env python3
"""
Tests para validar las validaciones de usuarios duplicados
"""

import pytest
import requests
import json
import sys
import os

# Configuración
BASE_URL = "http://localhost:5000/api/auth"
HEADERS = {"Content-Type": "application/json"}

class TestValidacionesUsuarios:
    """Clase para probar las validaciones de usuarios"""
    
    def test_registro_usuario_valido(self):
        """Probar registro de usuario válido"""
        data = {
            "username": "testuser_valido",
            "email": "test_valido@example.com",
            "password": "Password123"
        }
        
        response = requests.post(f"{BASE_URL}/register", json=data, headers=HEADERS)
        
        assert response.status_code == 201
        result = response.json()
        assert result['message'] == 'Usuario registrado exitosamente'
        assert result['user']['username'] == 'testuser_valido'
        assert result['user']['email'] == 'test_valido@example.com'
    
    def test_registro_username_duplicado(self):
        """Probar registro con username duplicado"""
        data = {
            "username": "testuser_valido",  # Usuario que ya existe
            "email": "test_duplicado@example.com",
            "password": "Password123"
        }
        
        response = requests.post(f"{BASE_URL}/register", json=data, headers=HEADERS)
        
        assert response.status_code == 400
        result = response.json()
        assert 'username' in result['error'].lower()
        assert 'uso' in result['error'].lower()
    
    def test_registro_email_duplicado(self):
        """Probar registro con email duplicado"""
        data = {
            "username": "testuser_nuevo",
            "email": "test_valido@example.com",  # Email que ya existe
            "password": "Password123"
        }
        
        response = requests.post(f"{BASE_URL}/register", json=data, headers=HEADERS)
        
        assert response.status_code == 400
        result = response.json()
        assert 'email' in result['error'].lower()
        assert 'registrado' in result['error'].lower()
    
    def test_registro_username_muy_corto(self):
        """Probar registro con username muy corto"""
        data = {
            "username": "ab",  # Muy corto
            "email": "test_corto@example.com",
            "password": "Password123"
        }
        
        response = requests.post(f"{BASE_URL}/register", json=data, headers=HEADERS)
        
        assert response.status_code == 400
        result = response.json()
        assert 'caracteres' in result['error'].lower()
    
    def test_registro_email_invalido(self):
        """Probar registro con email inválido"""
        data = {
            "username": "testuser_email",
            "email": "email-invalido",  # Email sin formato válido
            "password": "Password123"
        }
        
        response = requests.post(f"{BASE_URL}/register", json=data, headers=HEADERS)
        
        assert response.status_code == 400
        result = response.json()
        assert 'email' in result['error'].lower()
    
    def test_registro_password_muy_corta(self):
        """Probar registro con contraseña muy corta"""
        data = {
            "username": "testuser_password",
            "email": "test_password@example.com",
            "password": "123"  # Muy corta
        }
        
        response = requests.post(f"{BASE_URL}/register", json=data, headers=HEADERS)
        
        assert response.status_code == 400
        result = response.json()
        assert 'contraseña' in result['error'].lower()
        assert 'caracteres' in result['error'].lower()
    
    def test_check_username_disponible(self):
        """Probar verificación de username disponible"""
        data = {"username": "nuevousuario_disponible"}
        
        response = requests.post(f"{BASE_URL}/check-username", json=data, headers=HEADERS)
        
        assert response.status_code == 200
        result = response.json()
        assert result['available'] == True
        assert result['username'] == 'nuevousuario_disponible'
    
    def test_check_username_no_disponible(self):
        """Probar verificación de username no disponible"""
        data = {"username": "testuser_valido"}  # Usuario que ya existe
        
        response = requests.post(f"{BASE_URL}/check-username", json=data, headers=HEADERS)
        
        assert response.status_code == 200
        result = response.json()
        assert result['available'] == False
        assert result['username'] == 'testuser_valido'
    
    def test_check_email_disponible(self):
        """Probar verificación de email disponible"""
        data = {"email": "nuevo@example.com"}
        
        response = requests.post(f"{BASE_URL}/check-email", json=data, headers=HEADERS)
        
        assert response.status_code == 200
        result = response.json()
        assert result['available'] == True
        assert result['email'] == 'nuevo@example.com'
    
    def test_check_email_no_disponible(self):
        """Probar verificación de email no disponible"""
        data = {"email": "test_valido@example.com"}  # Email que ya existe
        
        response = requests.post(f"{BASE_URL}/check-email", json=data, headers=HEADERS)
        
        assert response.status_code == 200
        result = response.json()
        assert result['available'] == False
        assert result['email'] == 'test_valido@example.com'


def run_tests():
    """Ejecutar todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DE VALIDACIONES DE USUARIOS")
    print("=" * 60)
    
    test_instance = TestValidacionesUsuarios()
    tests_passed = 0
    total_tests = 0
    
    # Lista de métodos de prueba
    test_methods = [
        'test_registro_usuario_valido',
        'test_registro_username_duplicado',
        'test_registro_email_duplicado',
        'test_registro_username_muy_corto',
        'test_registro_email_invalido',
        'test_registro_password_muy_corta',
        'test_check_username_disponible',
        'test_check_username_no_disponible',
        'test_check_email_disponible',
        'test_check_email_no_disponible'
    ]
    
    for test_method in test_methods:
        total_tests += 1
        try:
            print(f"\n{total_tests}. {test_method}")
            getattr(test_instance, test_method)()
            print("✅ OK")
            tests_passed += 1
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    # Resumen
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN DE PRUEBAS")
    print(f"Pruebas pasadas: {tests_passed}/{total_tests}")
    print(f"Porcentaje de éxito: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("❌ Algunas pruebas fallaron")
        return 1


if __name__ == "__main__":
    try:
        exit_code = run_tests()
        sys.exit(exit_code)
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar al servidor")
        print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:5000")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
        sys.exit(1)
