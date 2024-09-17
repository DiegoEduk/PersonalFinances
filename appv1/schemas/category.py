from pydantic import BaseModel, Field
from typing import Optional

# Esquema para crear una nueva categoría
class CategoryCreate(BaseModel):
    category_name: str = Field(..., max_length=50)
    category_description: Optional[str] = Field(None, max_length=120)

# Esquema para actualizar una categoría
class CategoryUpdate(BaseModel):
    category_name: Optional[str] = Field(None, max_length=50)
    category_description: Optional[str] = Field(None, max_length=120)

# Esquema para devolver una categoría como respuesta
class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    category_description: Optional[str]
    category_status: int