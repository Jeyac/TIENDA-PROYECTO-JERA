#!/usr/bin/env python3
"""
Script para probar el chatbot con Socket.IO
"""
import socketio
import time
import json

# Crear cliente Socket.IO
sio = socketio.Client()

@sio.event
def connect():
    print("✅ Conectado al servidor de chat")
    print("💬 Puedes escribir mensajes para el chatbot")
    print("📝 Escribe 'exit' para salir")
    print("-" * 50)

@sio.event
def disconnect():
    print("❌ Desconectado del servidor")

@sio.event
def bot_response(data):
    print(f"🤖 Bot: {data.get('message', 'Sin respuesta')}")

@sio.event
def error(data):
    print(f"❌ Error: {data}")

def main():
    try:
        # Conectar al servidor
        sio.connect('http://localhost:5000')
        
        # Loop principal para enviar mensajes
        while True:
            try:
                message = input("👤 Tú: ").strip()
                
                if message.lower() in ['exit', 'salir', 'quit']:
                    break
                
                if message:
                    # Enviar mensaje al chatbot
                    sio.emit('ask', {'message': message})
                    print("⏳ Esperando respuesta...")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error al enviar mensaje: {e}")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    finally:
        sio.disconnect()
        print("👋 ¡Hasta luego!")

if __name__ == '__main__':
    main()
