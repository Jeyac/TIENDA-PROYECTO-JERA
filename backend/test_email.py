#!/usr/bin/env python3
import sys
import os

# Agregar el directorio del backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from funcionalidades.auth.infrastructure.email_service import EmailService
    print("✅ EmailService importado correctamente")
    
    # Crear instancia
    email_service = EmailService()
    print("✅ EmailService instanciado correctamente")
    
    # Probar envío simulado
    result = email_service.send_password_reset_email("test@example.com", "Test User", "test_token_123")
    print(f"✅ Resultado del envío: {result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()







