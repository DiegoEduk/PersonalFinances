from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from appv1.crud.permissions import get_permissions
from appv1.crud.users import create_user_sql, delete_user, get_all_users, get_all_users_paginated, get_user_by_email, get_user_by_id, update_user
from appv1.routers.login import get_current_user
from appv1.schemas.user import PaginatedUsersResponse, UserCreate, UserResponse, UserUpdate
from core.utils import process_and_save_image
from db.database import get_db

router = APIRouter()
MODULE = 'usuarios'

@router.post("/create")
async def insert_user(
    full_name: str = Form(...),
    mail: str = Form(...),
    user_role: str = Form(...),
    passhash: str = Form(...),
    file_img: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_insert:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    if current_user.user_role != 'SuperAdmin':
        if user_role == 'SuperAdmin':
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    # Verificar si el email ya está registrado
    existing_user = get_user_by_email(db, mail)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Llamamos a la función para procesar y guardar la imagen
    try:
        file_path = process_and_save_image(file_img)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    # Crear el objeto `UserCreate`
    user = UserCreate(
        full_name=full_name,
        mail=mail,
        user_role=user_role,
        passhash=passhash
    )

    respuesta = create_user_sql(db, user, file_path)
    if respuesta:
        return {"mensaje": "usuario registrado con éxito"}
    else:
        raise HTTPException(status_code=500, detail="Error al registrar el usuario")
    
@router.get("/get-user-by-email/", response_model=UserResponse)
async def read_user_by_email(
    email: str, 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if current_user.mail != email:  # si el email es diferente 
        if not permisos.p_select:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    usuario = get_user_by_email(db, email)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

@router.get("/get-all/", response_model=List[UserResponse])
async def read_all_users(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    usuarios = get_all_users(db)
    if len(usuarios) == 0:
        raise HTTPException(status_code=404, detail="No hay usuarios")
    
    return usuarios

# Endpoint para actualizar un usuario
@router.put("/update/", response_model=dict)
def update_user_by_id(
    user_id: str, 
    full_name: str = Form(...),
    mail: str = Form(...),
    user_role: str = Form(...),
    file_img: UploadFile = File(None), # ahora es 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if user_id != current_user.user_id:
        if not permisos.p_update:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
    verify_user = get_user_by_id(db, user_id)
    if verify_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if verify_user.mail != mail:
        # si cambia el email, verificar que el nuevo email no exista
        verify_new_email = get_user_by_email(db, mail)
        if verify_new_email:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Crear el objeto `UserUpdate`
    user = UserUpdate(
        full_name=full_name,
        mail=mail,
        user_role=user_role,
        user_status=verify_user.user_status
    )
    
    # Si se proporciona una nueva imagen, procesarla
    if file_img:
        try:
            file_path = process_and_save_image(file_img)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
    else:
        file_path = None

    db_user = update_user(db, user_id, user, file_path)
    if db_user:
        return {"mensaje": "registro actualizado con éxito" }

# usuarios paginados
@router.get("/users-by-page/", response_model=PaginatedUsersResponse)
def get_all_users_by_page(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    users, total_pages = get_all_users_paginated(db, page, page_size)

    return {
        "users": users,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size
    }

@router.delete("/delete/{user_id}", response_model=dict)
def delete_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if user_id != current_user.user_id:
        if not permisos.p_delete:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    result = delete_user(db, user_id)
    if result:
        return {"mensaje": "Usuario eliminado con éxito"}

