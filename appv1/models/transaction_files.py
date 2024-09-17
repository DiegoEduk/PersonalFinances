from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from appv1.models.base_class import Base

class TransactionFiles(Base):
    __tablename__ = "transactions_files"
    file_transactions_id = Column(Integer, primary_key=True, index=True)
    transactions_id = Column(Integer, ForeignKey("transactions.transactions_id"))
    file_url = Column(String(255), index=True)

    # Define la relación si es necesario
    transaction = relationship("Transaction")
