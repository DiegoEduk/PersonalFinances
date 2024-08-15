# Importaciones necesarias
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Funciones CRUD y consultas adicionales usando SQL crudo

# Consultar un usuario por su ID
def get_user_by_id(db: Session, user_id: str):
    sql = text("SELECT * FROM users WHERE user_id = :user_id")
    result = db.execute(sql, {"user_id": user_id}).fetchone()
    return result

# Consultar un usuario por su email
def get_user_by_email_raw(db: Session, mail: str):
    sql = text("SELECT * FROM users WHERE mail = :mail")
    result = db.execute(sql, {"mail": mail}).fetchone()
    return result

# Consultar todos los usuarios activos
def get_all_users_raw(db: Session):
    sql = text("SELECT * FROM users WHERE user_status = true")
    result = db.execute(sql).fetchall()
    return result

def get_all_users_paginated(db: Session, page: int = 1, page_size: int = 10):
    try:
        # Calcular el offset basado en el número de página y el tamaño de página
        offset = (page - 1) * page_size

        # Consulta SQL con paginación, incluyendo todos los campos requeridos
        sql = text(
            "SELECT user_id, full_name, mail, user_role, user_status, created_at, updated_at "
            "FROM users "
            "ORDER BY created_at DESC "  # Cambia esto por tu criterio de ordenación
            "LIMIT :page_size OFFSET :offset"
        )
        params = {
            "page_size": page_size,
            "offset": offset
        }
        result = db.execute(sql, params).fetchall()

        return result
    except SQLAlchemyError as e:
        print(f"Error al obtener todos los usuarios: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener todos los usuarios")

# Consultar todos los usuarios por su rol
def get_users_by_role_raw(db: Session, user_role: str):
    sql = text("SELECT * FROM users WHERE user_role = :user_role")
    result = db.execute(sql, {"user_role": user_role}).fetchall()
    return result

# Consultar solo nombre, correo y rol de un usuario
def get_user_name_and_email_raw(db: Session, user_id: str):
    sql = text("SELECT full_name, mail, user_role FROM users WHERE user_id = :user_id")
    result = db.execute(sql, {"user_id": user_id}).fetchone()
    return result

# Consultar todos los usuarios por rol y creados en un rango de fechas
def get_users_by_role_and_date_range_raw(db: Session, user_role: str, start_date: datetime, end_date: datetime):
    sql = text(
    "SELECT * FROM users "
    "WHERE user_role = :user_role AND created_at BETWEEN :start_date AND :end_date"
    )
    params = {
            "user_role": user_role,
            "start_date": start_date,
            "end_date": end_date
        }
    result = db.execute(sql, params).fetchall()
    return result

# Contar usuarios activos
def count_active_users_raw(db: Session):
    sql = "SELECT COUNT(user_id) FROM users WHERE user_status = TRUE"
    result = db.execute(sql).scalar()
    return result

# Crear un usuario
def create_user_raw(db: Session, user_id: str, full_name: str, mail: str, passhash: str, user_role: str):
    sql_query = text(
        "INSERT INTO users (user_id, full_name, mail, passhash, user_role) "
        "VALUES (:user_id, :full_name, :mail, :passhash, :user_role)"
    )
    params = {
        "user_id": user_id,
        "full_name": full_name,
        "mail": mail,
        "passhash": passhash,
        "user_role": user_role,
    }
    db.execute(sql_query, params)
    db.commit()
    return True  # Retorna True si la inserción fue exitosa
   
def create_user_raw2(db: Session, user_id: str, full_name: str, mail: str, passhash: str, user_role: str):
    try:
        sql_query = text(
            "INSERT INTO users (user_id, full_name, mail, passhash, user_role) "
            "VALUES (:user_id, :full_name, :mail, :passhash, :user_role)"
        )
        params = {
            "user_id": user_id,
            "full_name": full_name,
            "mail": mail,
            "passhash": passhash,
            "user_role": user_role,
        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear usuario: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El ID de usuario ya está en uso")
            if 'for key \'mail\'' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El email ya está registrado")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear usuario")
    except SQLAlchemyError as e:
        db.rollback()  
        print(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al crear usuario")

# Actualizar un usuario
def update_user_raw(db: Session, user_id: str, full_name: str = None, mail: str = None, passhash: str = None, user_role: str = None, user_status: bool = None):
    sql = "UPDATE users SET "
    params = {"user_id": user_id}
    updates = []
    if full_name:
        updates.append("full_name = :full_name")
        params["full_name"] = full_name
    if mail:
        updates.append("mail = :mail")
        params["mail"] = mail
    if passhash:
        updates.append("passhash = :passhash")
        params["passhash"] = passhash
    if user_role:
        updates.append("user_role = :user_role")
        params["user_role"] = user_role
    if user_status is not None:
        updates.append("user_status = :user_status")
        params["user_status"] = user_status
    sql += ", ".join(updates) + " WHERE user_id = :user_id"
    db.execute(sql, params)
    db.commit()

# Eliminar un usuario
def delete_user_raw(db: Session, user_id: str):
    sql = "DELETE FROM users WHERE user_id = :user_id"
    db.execute(sql, {"user_id": user_id})
    db.commit()
