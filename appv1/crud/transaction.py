from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import text
from fastapi import HTTPException
from appv1.schemas.transaction import TransactionCreate, TransactionUpdate

# Función para crear una transacción
def create_transaction(db: Session, transaction: TransactionCreate):
    try:
        sql_query = text(
            "INSERT INTO transactions (user_id, category_id, amount, t_description, t_type, t_date) "
            "VALUES (:user_id, :category_id, :amount, :t_description, :t_type, :t_date)"
        )
        params = {
            "user_id": transaction.user_id,
            "category_id": transaction.category_id,
            "amount": transaction.amount,
            "t_description": transaction.t_description,
            "t_type": transaction.t_type,
            "t_date": transaction.t_date
        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa
    
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad
        print(f"Error al crear transacción: {e}")
        raise HTTPException(status_code=400, detail="Error de integridad al crear transacción.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear transacción: {e}")
        raise HTTPException(status_code=500, detail="Error al crear transacción.")

# Función para leer transacciones
def update_transaction(db: Session, transaction_id: int, updates: TransactionUpdate):
    try:
        # Inicia la consulta SQL
        sql = "UPDATE transactions SET "
        params = {"transaction_id": transaction_id}
        update_fields = []

        # Verifica qué campos se deben actualizar y construye la consulta y parámetros
        if updates.user_id is not None:
            update_fields.append("user_id = :user_id")
            params["user_id"] = updates.user_id
        if updates.category_id is not None:
            update_fields.append("category_id = :category_id")
            params["category_id"] = updates.category_id
        if updates.amount is not None:
            update_fields.append("amount = :amount")
            params["amount"] = updates.amount
        if updates.t_description is not None:
            update_fields.append("t_description = :t_description")
            params["t_description"] = updates.t_description
        if updates.t_type is not None:
            update_fields.append("t_type = :t_type")
            params["t_type"] = updates.t_type
        if updates.t_date is not None:
            update_fields.append("t_date = :t_date")
            params["t_date"] = updates.t_date
        
        # Si no se especifica ningún campo, lanzar un error
        if not update_fields:
            raise HTTPException(status_code=400, detail="No se especificaron campos para actualizar.")
        
        # Concatena los campos de actualización con comas
        sql += ", ".join(update_fields)
        sql += " WHERE transactions_id = :transaction_id"

        # Envuelve la consulta SQL en text()
        sql = text(sql)

        # Ejecuta la consulta
        result = db.execute(sql, params)
        db.commit()
        
        # Si registros afectados es igual a cero no encontró el id
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transacción no encontrada para actualizar.")
        
        return True
    
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad
        print(f"Error al actualizar transacción: {e}")
        raise HTTPException(status_code=400, detail="Error de integridad al actualizar transacción.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al actualizar transacción: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar transacción.")

# Función para eliminar una transacción
def delete_transaction(db: Session, transaction_id: int):
    try:
        sql_query = text(
            "DELETE FROM transactions WHERE transactions_id = :transaction_id"
        )
        result = db.execute(sql_query, {"transaction_id": transaction_id})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transacción no encontrada para eliminar.")
        return True
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al eliminar transacción: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar transacción.")

# Obtiene las transacciones de un usuario en un rango de fechas
def get_transactions_by_user_and_date_range(db: Session, user_id: str, start_date: str, end_date: str):
    try:
        sql_query = text(
            "SELECT * FROM transactions "
            "WHERE user_id = :user_id "
            "AND t_date BETWEEN :start_date AND :end_date"
        )
        params = {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date
        }
        result = db.execute(sql_query, params).mappings().all()
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron transacciones en el rango de fechas especificado.")
        return result
    
    except SQLAlchemyError as e:
        print(f"Error al obtener transacciones: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener transacciones.")


def insert_file_to_db(db: Session, transactions_id: int, file_url: str):
    try:
        sql_query = text(
            "INSERT INTO transactions_files (transactions_id, file_url) "
            "VALUES (:transactions_id, :file_url)"
        )
        params = {
            "transactions_id": transactions_id,
            "file_url": file_url
        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa
    
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al insertar archivo: {e}")
        raise HTTPException(status_code=400, detail="Error de integridad al insertar archivo.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al insertar archivo: {e}")
        raise HTTPException(status_code=500, detail="Error al insertar archivo.")





# Obtiene las transacciones en un rango de fechas
def get_transactions_by_date_range(db: Session, start_date: str, end_date: str):
    try:
        sql_query = text(
            "SELECT * FROM transactions "
            "WHERE t_date BETWEEN :start_date AND :end_date"
        )
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        result = db.execute(sql_query, params).mappings().all()
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron transacciones en el rango de fechas especificado.")
        return result
    
    except SQLAlchemyError as e:
        print(f"Error al obtener transacciones: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener transacciones.")
