from pydantic import BaseModel
from datetime import date
from typing import Optional
import enum

class TransactionType(str, enum.Enum):
    revenue = "revenue"
    expenses = "expenses"

class TransactionBase(BaseModel):
    transactions_id: Optional[int] = None
    user_id: str
    category_id: int
    amount: float
    t_description: str
    t_type: TransactionType
    t_date: date

class TransactionCreate(TransactionBase):
    pass
