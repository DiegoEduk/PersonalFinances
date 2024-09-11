import secrets
import string
from fastapi import HTTPException
from PIL import Image
import uuid
import os

# Función para generar un ID de usuario aleatorio
def generate_user_id(length=30):
    # Caracteres posibles para el ID aleatorio
    characters = string.ascii_letters + string.digits
    # Genera un ID aleatorio de la longitud deseada
    random_id = ''.join(secrets.choice(characters) for _ in range(length))

    return random_id

# Carpeta donde se guardarán las imágenes
UPLOAD_DIRECTORY = "./static/images/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Función para procesar y guardar la imagen
def process_and_save_image(file):
    # Validar tipo de archivo
    valid_content_types = ['image/jpeg', 'image/png']
    valid_extensions = ['.jpg', '.jpeg', '.png']

    # Verificar el tipo de archivo según su content_type
    if file.content_type not in valid_content_types:
        raise HTTPException(status_code=400, detail="Formato inválido. Solo JPEG y PNG.")
    
    # Verificar la extensión del archivo si es necesario
    extension = os.path.splitext(file.filename)[1].lower()  # Obtener la extensión y convertir a minúsculas
    if extension not in valid_extensions:
        raise HTTPException(status_code=400, detail="Extension inválida. Solo .jpg, .jpeg, y .png")
    
    # Generar un nombre único para la imagen (siempre guardamos como .jpg)
    unique_filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    # Abrir y procesar la imagen con Pillow
    image = Image.open(file.file)
    image = image.convert("RGB")  # Convertir a formato RGB si es necesario

    # Comprimir la imagen antes de almacenarla
    image.save(file_path, "JPEG", quality=85)  # Guardar como JPEG con un 85% de calidad

    return file_path  # Devolver la ruta donde se guardó la imagen
