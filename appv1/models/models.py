# from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, Enum, DateTime, TIMESTAMP, Date, CHAR
# from sqlalchemy.orm import relationship
# from models.base_class import Base
# import enum
# from datetime import datetime

# class TransactionType(enum.Enum):
#     revenue = "revenue"
#     expenses = "expenses"

# class Role(Base):
#     __tablename__ = 'roles'
#     rol_name = Column(String(15), primary_key=True)

# class Module(Base):
#     __tablename__ = 'modules'
#     module_name = Column(String(15), primary_key=True)

# class Permission(Base):
#     __tablename__ = 'permissions'
#     rol_name = Column(String(15), ForeignKey('roles.rol_name'), primary_key=True)
#     module_name = Column(String(15), ForeignKey('modules.module_name'), primary_key=True)
#     p_select = Column(Boolean, default=True)
#     p_insert = Column(Boolean, default=True)
#     p_update = Column(Boolean, default=True)
#     p_delete = Column(Boolean, default=True)

#     role = relationship("Role")
#     module = relationship("Module")

# class User(Base):
#     __tablename__ = 'users'
#     user_id = Column(CHAR(30), primary_key=True)
#     full_name = Column(String(80))
#     mail = Column(String(100), unique=True)
#     passhash = Column(String(140))
#     user_role = Column(String(15), ForeignKey('roles.rol_name'))
#     user_status = Column(Boolean, default=True)
#     created_at = Column(TIMESTAMP, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# class Category(Base):
#     __tablename__ = 'category'
#     category_id = Column(Integer, primary_key=True, autoincrement=True)
#     category_name = Column(String(50))
#     category_description = Column(String(120))
#     category_status = Column(Boolean, default=True)

# class Transaction(Base):
#     __tablename__ = 'transactions'
#     transactions_id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(CHAR(30), ForeignKey('users.user_id'))
#     category_id = Column(Integer, ForeignKey('category.category_id'))
#     amount = Column(Float(10, 2))
#     t_description = Column(String(120))
#     t_type = Column(Enum(TransactionType))
#     t_date = Column(Date)

#     user = relationship("User")
#     category = relationship("Category")
