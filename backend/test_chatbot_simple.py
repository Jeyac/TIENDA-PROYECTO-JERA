#!/usr/bin/env python3
"""
Script simple para probar el chatbot sin Socket.IO
"""
import requests
import json

def test_chatbot_api():
    """Probar el chatbot a través de la API REST"""
    base_url = "http://localhost:5000"
    
    print("🤖 Probando el chatbot...")
    print("-" * 50)
    
    # Probar endpoint de salud
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            print(f"📊 Estado: {response.json()}")
        else:
            print(f"❌ Error en servidor: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("💡 Asegúrate de ejecutar: python app.py")
        return
    
    # Probar endpoint de RAG (recuperar contexto)
    print("\n🧠 Probando RAG (Recuperación de contexto)...")
    try:
        rag_data = {
            "query": "¿Cómo puedo hacer un pedido?"
        }
        response = requests.post(f"{base_url}/api/rag/retrieve", json=rag_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ RAG funcionando correctamente")
            print(f"📝 Contexto encontrado: {len(result.get('chunks', []))} fragmentos")
            if result.get('chunks'):
                print(f"📄 Primer fragmento: {result['chunks'][0][:100]}...")
        else:
            print(f"⚠️ RAG no disponible: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error en RAG: {e}")
    
    # Probar endpoint de FAQ
    print("\n❓ Probando FAQ...")
    try:
        response = requests.get(f"{base_url}/api/faq/")
        if response.status_code == 200:
            faqs = response.json()
            print("✅ FAQ funcionando correctamente")
            print(f"📋 Preguntas frecuentes disponibles: {len(faqs)}")
            if faqs:
                print(f"❓ Primera FAQ: {faqs[0].get('pregunta', 'N/A')}")
        else:
            print(f"⚠️ FAQ no disponible: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error en FAQ: {e}")
    
    # Probar endpoint de productos
    print("\n🛍️ Probando productos...")
    try:
        response = requests.get(f"{base_url}/api/productos/")
        if response.status_code == 200:
            productos = response.json()
            print("✅ Productos funcionando correctamente")
            print(f"📦 Productos disponibles: {len(productos)}")
        else:
            print(f"⚠️ Productos no disponibles: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error en productos: {e}")
    
    # Probar endpoint de categorías
    print("\n📂 Probando categorías...")
    try:
        response = requests.get(f"{base_url}/api/categorias/")
        if response.status_code == 200:
            categorias = response.json()
            print("✅ Categorías funcionando correctamente")
            print(f"📁 Categorías disponibles: {len(categorias)}")
        else:
            print(f"⚠️ Categorías no disponibles: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error en categorías: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Para probar el chat en tiempo real:")
    print("1. Asegúrate de que el servidor esté ejecutándose")
    print("2. Abre el navegador en http://localhost:5000")
    print("3. O usa el script test_chatbot.py con Socket.IO")
    print("=" * 50)

if __name__ == '__main__':
    test_chatbot_api()




