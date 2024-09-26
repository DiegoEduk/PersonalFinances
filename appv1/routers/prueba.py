from fastapi import APIRouter, Depends, File, UploadFile
from core.utils import save_file
from db.database import get_db
from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy.orm import Session
from appv1.crud.prueba import insertar_usuario, insertar_comprobante_pago  # Asegúrate de importar tus funciones de inserción


router = APIRouter()

# Función para leer el archivo Excel y almacenar los datos
def almacenar_usuarios_desde_excel(db: Session, ruta_archivo_excel: str):
    # Leer el archivo Excel
    df = pd.read_excel(ruta_archivo_excel)

    # Suponiendo que el archivo tiene columnas 'nombre', 'correo', 'direccion', 'telefono', 'url_comprobante_pago'
    for index, row in df.iterrows():
        # Insertar datos en la tabla 'usuarios'
        nuevo_usuario = insertar_usuario(
            db=db,
            tipo_doc=row['tipo_documento'], 
            num_doc=row['documento'], 
            nombres=row['nombres'],
            apellidos=row['apellidos'],
            correo=row['correo'], 
            telefono=row.get('celular', None)
        )

        # Insertar solo el campo 'url_comprobante_pago' en la tabla 'comprobantes_pago'
        insertar_comprobante_pago(
            db=db, 
            usuario_id=nuevo_usuario.id, 
            url_comprobante_pago=row['url_comprobante_pago']
        )

    return {"message": "Datos almacenados correctamente desde el archivo Excel."}


# Endpoint para subir el archivo y procesar los datos
@router.post("/upload-excel/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Guardar el archivo
    file_location = save_file(file)
    
    # Procesar y almacenar datos en la base de datos
    almacenar_usuarios_desde_excel(db, file_location)
    
    return {"message": "File processed and data stored successfully.", "file_location": file_location}

