import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from funcionalidades.core.infraestructura.auth import jwt_required

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file):
    file.seek(0, 2)  # Mover al final del archivo
    size = file.tell()
    file.seek(0)  # Volver al inicio
    return size

image_bp = Blueprint('images', __name__)

@image_bp.route('/upload', methods=['OPTIONS'])
def upload_image_options():
    """Manejar preflight CORS para subida de imágenes"""
    return jsonify({'message': 'OK'}), 200

@image_bp.route('/upload', methods=['POST'])
@jwt_required(roles={'administrador'})
def upload_image():
    """Subir imagen para producto"""
    
    try:
        print("DEBUG: Endpoint de subida de imágenes llamado")
        print("DEBUG: Iniciando subida de imagen")
        print("DEBUG: Archivos recibidos:", request.files)
        print("DEBUG: Headers:", dict(request.headers))
        print("DEBUG: Method:", request.method)
        
        # Verificar que se envió un archivo
        if 'image' not in request.files:
            print("DEBUG: No se encontró archivo 'image'")
            return jsonify({'error': 'No se proporcionó ningún archivo'}), 400
        
        file = request.files['image']
        print("DEBUG: Archivo obtenido:", file.filename)
        
        # Verificar que se seleccionó un archivo
        if file.filename == '':
            print("DEBUG: Nombre de archivo vacío")
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        # Verificar tipo de archivo
        print("DEBUG: Verificando tipo de archivo:", file.filename)
        if not allowed_file(file.filename):
            print("DEBUG: Tipo de archivo no permitido")
            return jsonify({'error': f'Tipo de archivo no permitido. Tipos permitidos: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Verificar tamaño del archivo
        print("DEBUG: Verificando tamaño del archivo")
        file_size = get_file_size(file)
        print("DEBUG: Tamaño del archivo:", file_size)
        if file_size > MAX_FILE_SIZE:
            print("DEBUG: Archivo demasiado grande")
            return jsonify({'error': f'El archivo es demasiado grande. Tamaño máximo: {MAX_FILE_SIZE // (1024*1024)}MB'}), 400
        
        # Generar nombre único para el archivo
        print("DEBUG: Generando nombre único")
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        print("DEBUG: Nombre único generado:", unique_filename)
        
        # Crear directorio de uploads si no existe
        print("DEBUG: Creando directorio de uploads")
        upload_folder = os.path.join(current_app.root_path, 'uploads', 'products')
        print("DEBUG: Directorio de uploads:", upload_folder)
        os.makedirs(upload_folder, exist_ok=True)
        
        # Guardar archivo
        print("DEBUG: Guardando archivo")
        file_path = os.path.join(upload_folder, unique_filename)
        print("DEBUG: Ruta completa del archivo:", file_path)
        file.save(file_path)
        print("DEBUG: Archivo guardado exitosamente")
        
        # Generar URL relativa
        image_url = f"/uploads/products/{unique_filename}"
        print("DEBUG: URL generada:", image_url)
        
        return jsonify({
            'message': 'Imagen subida correctamente',
            'filename': unique_filename,
            'url': image_url,
            'size': file_size
        })
        
    except Exception as e:
        print(f"Error subiendo imagen: {e}")
        return jsonify({'error': str(e)}), 500

@image_bp.route('/<filename>')
def serve_image(filename):
    """Servir imágenes subidas"""
    try:
        upload_folder = os.path.join(current_app.root_path, '..', 'uploads', 'products')
        file_path = os.path.join(upload_folder, secure_filename(filename))
        
        if os.path.exists(file_path):
            from flask import send_file
            return send_file(file_path)
        else:
            return jsonify({'error': 'Imagen no encontrada'}), 404
            
    except Exception as e:
        print(f"Error sirviendo imagen: {e}")
        return jsonify({'error': str(e)}), 500
