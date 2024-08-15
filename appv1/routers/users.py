# from typing import List
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from appv1.crud.users import update_user
# from appv1.crud.usersSQL import create_user_raw, create_user_raw2, get_all_users_paginated, get_all_users_raw, get_user_by_id_raw
# from appv1.crud.usersORM import create_user

# from appv1.schemas.user import PaginatedUsersResponse, UserCreate, UserResponse, UserUpdate
# from db.database import get_db

# router = APIRouter()

# # Endpoint para crear un usuario
# @router.post("/create/", response_model=dict)
# def insert_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = create_user_raw2(
#         db,
#         user.user_id,
#         user.full_name,
#         user.mail,
#         user.passhash,
#         user.user_role
#     )
#     return {"mensaje":"registro almacenado con éxito"}

# @router.get("/get-by-id/", response_model=UserResponse)
# def read_by_id(user_id: str, db: Session = Depends(get_db)):
#     return get_user_by_id_raw(db, user_id)

# @router.get("/get-all/", response_model=List[UserResponse])
# def read_all( db: Session = Depends(get_db)):
#     return get_all_users_raw(db)

# @router.get("/get-all-paginated/", response_model=List[UserResponse])
# def read_all(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     users = get_all_users_paginated(db, page, page_size)
#     return users

# # Endpoint para actualizar un usuario
# @router.put("/update/", response_model=dict)
# def update_user_by_id(user: UserUpdate, db: Session = Depends(get_db)):
#     db_user = update_user(db, user)
#     if db_user:
#         return {"mensaje":"registro actualizado con éxito"}

# # usuarios paginados
# @router.get("/users-by-page/", response_model=PaginatedUsersResponse)
# def get_all_users_by_page(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    
#     users, total_pages = get_all_users_paginated(db, page, page_size)

#     # Convertir el resultado a una lista de diccionarios
#     users_list = [dict(user) for user in users]

#     return {
#         "users": users_list,
#         "total_pages": total_pages,
#         "current_page": page,
#         "page_size": page_size
#     }
