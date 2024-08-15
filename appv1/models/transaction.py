from sqlalchemy import Column, String, Integer, Float, Enum, Date, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from appv1.models.base_class import Base
import enum

class TransactionType(enum.Enum):
    revenue = "revenue"
    expenses = "expenses"

class Transaction(Base):
    __tablename__ = 'transactions'
    transactions_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(30), ForeignKey('users.user_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    amount = Column(Float(10, 2))
    t_description = Column(String(120))
    t_type = Column(Enum(TransactionType))
    t_date = Column(Date)

    user = relationship("User")
    category = relationship("Category")
