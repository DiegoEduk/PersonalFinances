from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import Dict, List
from appv1.crud.permissions import get_permissions
from appv1.schemas.transaction import TransactionCreate, TransactionTypeEnum, TransactionUpdate, TransactionResponse
from appv1.crud.transaction import create_transaction, insert_file_to_db, sumar_numeros_procedimiento, update_transaction, delete_transaction, get_transactions_by_user_and_date_range
from appv1.schemas.user import UserResponse
from appv1.routers.login import get_current_user
from core.utils import save_file
from db.database import get_db  # Importar tu función para obtener la sesión de la DB

# Crear el router para las rutas de transacciones
router = APIRouter()
MODULE = 'transacciones'

# Ruta para crear una nueva transacción
@router.post("/create", response_model=dict)
async def create_transaction_route(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_insert:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    result = create_transaction(db, transaction)
    if result:
        return {"mensaje": "transacción creada con éxito"}  # Si la creación fue exitosa, retornamos un mensaje
    raise HTTPException(status_code=500, detail="Error al crear la transacción")

# Ruta para actualizar una transacción por ID
@router.put("/update/{transaction_id}", response_model=dict)
async def update_transaction_route(
    transaction_id: int,
    updates: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_update:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    result = update_transaction(db, transaction_id, updates)
    if result:
        return {"mensaje": "transacción actualizada con éxito"}
    raise HTTPException(status_code=500, detail="Error al actualizar la transacción")

# Ruta para eliminar una transacción por ID
@router.delete("/delete/{transaction_id}", response_model=dict)
async def delete_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_delete:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    result = delete_transaction(db, transaction_id)
    if result:
        return {"mensaje": "transacción eliminada con éxito"}
    raise HTTPException(status_code=500, detail="Error al eliminar la transacción")

# Ruta para obtener las transacciones de un usuario en un rango de fechas
@router.get("/get-by-user-and-date", response_model=List[TransactionResponse])
async def get_transactions_by_user_and_date_range_route(
    user_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    transactions = get_transactions_by_user_and_date_range(db, user_id, start_date, end_date)
    if transactions:
        return transactions
    raise HTTPException(status_code=404, detail="No se encontraron transacciones en el rango de fechas especificado.")

@router.post("/upload-file/")
async def upload_file(
    transactions_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """ Maneja la subida de archivos y la inserción en la base de datos. """
    # Guarda el archivo y obtiene la ruta completa del archivo
    try:
        file_location = save_file(file)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    # Inserta la referencia del archivo en la base de datos
    success = insert_file_to_db(db, transactions_id, file_location)
    
    if success:
        return {"mensaje": "archivo almacenado con éxito"}


# Ruta para sumar dos números usando el procedimiento almacenado
@router.get("/sumar")
async def sumar_numeros_route(
    num1: int,
    num2: int,
    db: Session = Depends(get_db)
):
    # Llamar a la función que ejecuta el procedimiento almacenado
    resultado = sumar_numeros_procedimiento(db, num1, num2)
    
    if resultado:
        return resultado
    raise HTTPException(status_code=404, detail="No se pudo obtener el resultado de la suma.")