from sqlalchemy.orm import Session
import models, schemas

def get_roles(db: Session):
    return db.query(models.Role).all()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(rol_name=role.rol_name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, name_role: str, role: schemas.RoleCreate):
    db_role = db.query(models.Role).filter(models.Role.rol_name == name_role).first()
    if db_role:
        db_role.rol_name = role.rol_name
        db.commit()
        db.refresh(db_role)
        return db_role
    

