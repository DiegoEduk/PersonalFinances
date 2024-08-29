from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# consultar permisos de un rol por modulo
def get_permissions(db: Session, rol: str, module: str):
    try:
        sql = text("SELECT p_select, p_insert, p_update, p_delete FROM permissions WHERE rol_name = :rol AND module_name = :module")
        result = db.execute(sql, {"rol": rol, "module": module}).fetchone()
        return result
    except SQLAlchemyError as e:
        print(f"Error al obtener permisos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener permisos")

# consultar todos los permisos de un rol
def get_all_permissions(db: Session, rol: str):
    try:
        sql = text("SELECT module_name, p_select FROM permissions WHERE rol_name = :rol")
        result = db.execute(sql, {"rol": rol}).mappings().all()
        return result
    except SQLAlchemyError as e:
        print(f"Error al obtener permisos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener permisos")
