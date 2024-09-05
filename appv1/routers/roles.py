from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from appv1.crud.permissions import get_permissions
from appv1.crud.role import get_roles
from appv1.routers.login import get_current_user
from appv1.schemas.role import RoleBase
from appv1.schemas.user import UserResponse
from db.database import get_db

router = APIRouter()
MODULE = 'roles'

@router.get("/get-all/", response_model=List[RoleBase])
async def read_all_roles(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    roles = get_roles(db)
    if len(roles) == 0:
        raise HTTPException(status_code=404, detail="No hay usuarios")
    
    return roles
