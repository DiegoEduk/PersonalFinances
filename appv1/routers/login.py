from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from appv1.crud.permissions import get_all_permissions, get_permissions
from appv1.crud.users import create_user_sql, delete_user, get_all_users, get_all_users_paginated, get_user_by_email, get_user_by_id, update_user
from appv1.schemas.user import PaginatedUsersResponse, ResponseLoggin, UserCreate, UserLoggin, UserRegister, UserResponse, UserUpdate
from core.security import create_access_token, verify_password, verify_token
from db.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/access/token")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    user = await verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_db = get_user_by_id(db, user)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_db.user_status:
        raise HTTPException(status_code=403, detail="User Deleted, Not authorized")
    return user_db

def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.passhash):
        return False
    return user

@router.post("/token", response_model=ResponseLoggin)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Datos Incorrectos en email o password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.user_id, "rol":user.user_role}
    )

    permisos = get_all_permissions(db, user.user_role)

    return ResponseLoggin(
        user=UserLoggin(
            user_id=user.user_id,
            full_name=user.full_name,
            mail=user.mail,
            user_role=user.user_role
        ),
        permissions=permisos,
        access_token=access_token
    )

@router.post("/register")
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    user.user_role = 'Cliente'
    respuesta = create_user_sql(db, user)
    if respuesta:
        return {"mensaje":"usuario registrado con éxito"}
    

# @router.get("/login/", response_model=dict)
# async def access(email: str, password: str, db: Session = Depends(get_db)):
#     usuario = get_user_by_email(db, email)
#     if usuario is None:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")

#     result = verify_password(password, usuario.passhash)
#     if not result:
#         raise HTTPException(status_code=401, detail="Usuario no autorizado")

#     data = {"sub":usuario.user_id, "rol":usuario.user_role}
#     token = create_access_token(data)
#     return {"token":token}
