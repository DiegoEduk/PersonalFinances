from pydantic import BaseModel
from typing import Optional
from datetime import date
import enum

class TransactionTypeEnum(str, enum.Enum):
    revenue = "revenue"
    expenses = "expenses"

class TransactionBase(BaseModel):
    user_id: str
    category_id: int
    amount: float
    t_description: Optional[str] = None
    t_type: TransactionTypeEnum
    t_date: date

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    t_description: Optional[str] = None
    t_type: Optional[TransactionTypeEnum] = None
    t_date: Optional[date] = None

class TransactionResponse(TransactionBase):
    transactions_id: int
    category_name: str

class TransactionFilesResponse(BaseModel):
    file_url: int