# Importaciones necesarias
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
from appv1.models.user import User

# Funciones CRUD

# Consultar un usuario por su ID
def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

# Consultar un usuario por su email
def get_user_by_email(db: Session, mail: str):
    return db.query(User).filter(User.mail == mail).first()

# Consultar todos los usuarios
def get_all_users(db: Session):
    return db.query(User).all()

# Consultar todos los usuarios por su rol
def get_users_by_role(db: Session, user_role: str):
    return db.query(User).filter(User.user_role == user_role).all()

# Consultar solo nombre y correo de un usuario
def get_user_name_and_email(db: Session, user_id: str):
    return db.query(User.full_name, User.mail).filter(User.user_id == user_id).first()

# Consultar todos los usuarios por rol y creados en un rango de fechas
def get_users_by_role_and_date_range(db: Session, user_role: str, start_date: datetime, end_date: datetime):
    return db.query(User).filter(User.user_role == user_role, User.created_at >= start_date, User.created_at <= end_date).all()

# Contar usuarios activos
def count_active_users(db: Session):
    return db.query(func.count(User.user_id)).filter(User.user_status == True).scalar()

# Crear un usuario
def create_user(db: Session, user_id: str, full_name: str, mail: str, passhash: str, user_role: str):
    db_user = User(
        user_id=user_id, 
        full_name=full_name, 
        mail=mail, 
        passhash=passhash, 
        user_role=user_role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

# Crear un usuario
def create_user2(db: Session, user_id: str, full_name: str, mail: str, passhash: str, user_role: str):
    db_user = User(
        user_id=user_id, 
        full_name=full_name, 
        mail=mail, 
        passhash=passhash, 
        user_role=user_role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

# Actualizar un usuario
def update_user(db: Session, user_id: str, full_name: str = None, mail: str = None, passhash: str = None, user_role: str = None, user_status: bool = None):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        if full_name:
            db_user.full_name = full_name
        if mail:
            db_user.mail = mail
        if passhash:
            db_user.passhash = passhash
        if user_role:
            db_user.user_role = user_role
        if user_status is not None:
            db_user.user_status = user_status
        db.commit()
        db.refresh(db_user)
    return db_user

# Eliminar un usuario
def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user