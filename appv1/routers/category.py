from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from appv1.crud.category import create_category_sql, delete_category, get_all_active_categories, get_category_by_id, get_category_by_name, set_category_status, update_category
from appv1.crud.permissions import get_permissions
from appv1.routers.login import get_current_user
from appv1.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from appv1.schemas.user import UserResponse
from db.database import get_db  # Importar tu función para obtener la sesión de la DB


# Crear el router para las rutas de categoría
router = APIRouter()
MODULE = 'categorias'

# Ruta para crear una nueva categoría
@router.post("/create", response_model=dict)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_insert:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    result = create_category_sql(db, category)
    if result:
        return {"mensaje": "categoria registrada con éxito"}  # Si la creación fue exitosa, retornamos los datos de la categoría
    raise HTTPException(status_code=500, detail="Error al crear la categoría")

# Ruta para obtener una categoría por ID
@router.get("/get-by-id/{category_id}", response_model=CategoryResponse)
async def read_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    return get_category_by_id(db, category_id)

# Ruta para obtener todas las categorías activas
@router.get("/get-all", response_model=List[CategoryResponse])
async def read_active_categories(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    return get_all_active_categories(db)

# Ruta para actualizar una categoría por ID
@router.put("/update/{category_id}", response_model=dict)
async def update_category_route(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_update:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    result = update_category(db, category_id, category)
    if result:
        return {"mensaje": "registro actualizado con éxito" }
    
# Ruta para eliminar una categoría por ID
@router.delete("/delete/{category_id}", response_model=dict)
async def delete_category_route(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_delete:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    result = delete_category(db, category_id)
    if result:
        return {"mensaje": "registro eliminado con éxito" }
    raise HTTPException(status_code=500, detail="Error al eliminar la categoría")

# Ruta para activar o desactivar una categoría por ID
@router.put("/status/{category_id}")
def update_category_status(
    category_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Activa o desactiva una categoría según el valor de is_active.
    """
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_update:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    success = set_category_status(db, category_id, is_active)
    if success:
        return {"message": "El estado de la Categoría ha sido actualizado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al actualizar el estado de la categoría")

@router.get("/get-by-name/{category_name}", response_model=List[CategoryResponse])
async def read_category_by_name(
    category_name: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    category = get_category_by_name(db, category_name)
    if category:
        return category  # Devuelve los datos de la categoría