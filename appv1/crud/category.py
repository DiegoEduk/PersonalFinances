from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from appv1.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


def create_category_sql(db: Session, category: CategoryCreate):
    try:
        sql_query = text(
            "INSERT INTO category (category_name, category_description, category_status) "
            "VALUES (:category_name, :category_description, :category_status)"
        )
        params = {
            "category_name": category.category_name,
            "category_description": category.category_description,
            "category_status": 1,  # Por defecto, categoría activa
        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa
    
    except IntegrityError as e:
        db.rollback()
        print(f"Error al crear categoría: {e}")
        raise HTTPException(status_code=400, detail="Error al crear la categoría")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear categoría: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la categoría")


def get_category_by_id(db: Session, category_id: int):
    try:
        sql = text("SELECT * FROM category WHERE category_id = :category_id")
        result = db.execute(sql, {"category_id": category_id}).fetchone()
        if result:
            return result # Devolvemos los datos en el formato del esquema
        else:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    except SQLAlchemyError as e:
        print(f"Error al buscar categoría por ID: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar categoría")

def get_all_categories(db: Session):
    try:
        sql = text("SELECT * FROM category")
        result = db.execute(sql).mappings().all()
        return result  # Convertimos cada fila en un CategoryResponse
    except SQLAlchemyError as e:
        print(f"Error al buscar categorías activas: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar categorías activas")

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    try:
        sql = "UPDATE category SET "
        params = {"category_id": category_id}
        updates = []
        
        if category.category_name:
            updates.append("category_name = :category_name")
            params["category_name"] = category.category_name
        if category.category_description:
            updates.append("category_description = :category_description")
            params["category_description"] = category.category_description
        
        sql += ", ".join(updates) + " WHERE category_id = :category_id"
        sql = text(sql)
        
        db.execute(sql, params)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al actualizar categoría: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar categoría")

def delete_category(db: Session, category_id: int):
    try:
        sql = text("DELETE FROM category WHERE category_id = :category_id")
        db.execute(sql, {"category_id": category_id})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al eliminar categoría: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar categoría")

# Activa o desactiva una categoría según el valor de is_active.
def set_category_status(db: Session, category_id: int, is_active: bool):
    try:
        # Llamar a la función que obtiene la categoría por ID
        category = get_category_by_id(db, category_id)

        # Actualizar el estado de la categoría
        sql_update = text("UPDATE category SET category_status = :category_status WHERE category_id = :category_id")
        params = {
            "category_status": is_active,  # Activar o desactivar según el valor de is_active
            "category_id": category_id
        }
        db.execute(sql_update, params)
        db.commit()  # Confirmamos la transacción
        
        return True  # Retornamos True si la actualización fue exitosa
    
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad
        print(f"Error de integridad al actualizar el estado de la categoría: {e}")
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar el estado de la categoría")
    
    except SQLAlchemyError as e:
        db.rollback()  # Revertir la transacción en caso de otro error
        print(f"Error al actualizar el estado de la categoría: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el estado de la categoría")

def get_category_by_name(db: Session, category_name: str):
    try:
        # Usamos el operador LIKE para permitir búsquedas parciales
        sql = text("SELECT * FROM category WHERE category_name LIKE :category_name")
        # Añadimos los '%' para permitir coincidencias parciales al principio y al final
        result = db.execute(sql, {"category_name": f"%{category_name}%"}).fetchall()
        
        if result:
            return result  # Devolvemos los datos en el formato del esquema
        else:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    except SQLAlchemyError as e:
        print(f"Error al buscar categoría por nombre: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar categoría")