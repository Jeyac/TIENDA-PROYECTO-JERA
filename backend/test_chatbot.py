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

@sio.on('server_message')
def on_server_message(data):
    try:
        msg = (data or {}).get('message', str(data))
    except Exception:
        msg = str(data)
    print(f"ℹ️  Servidor: {msg}")

@sio.on('answer')
def on_answer(data):
    try:
        msg = (data or {}).get('message', str(data))
    except Exception:
        msg = str(data)
    print(f"🤖 Bot: {msg}")

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
