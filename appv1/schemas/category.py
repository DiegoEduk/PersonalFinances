from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    category_id: Optional[int] = None
    category_name: str
    category_description: str
    category_status: bool = True

class CategoryCreate(CategoryBase):
    pass

