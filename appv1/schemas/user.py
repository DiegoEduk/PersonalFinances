from typing import Annotated, List, Optional
from pydantic import BaseModel, EmailStr, StringConstraints
from datetime import datetime

class UserBase(BaseModel):
    full_name: Annotated[str, StringConstraints(max_length=80)]
    mail: EmailStr
    user_role: Annotated[str, StringConstraints(max_length=15)]

class UserCreate(UserBase):
    passhash: Annotated[str, StringConstraints(max_length=30)]
    
class UserResponse(UserBase):
    user_id: str
    user_status: bool = True
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    full_name: Optional[Annotated[str, StringConstraints(max_length=80)]] = None
    mail: Optional[EmailStr] = None
    user_role: Optional[Annotated[str, StringConstraints(max_length=15)]] = None
    user_status: bool = None
    
class PaginatedUsersResponse(BaseModel):
    users: List[UserResponse]
    total_pages: int
    current_page: int
    page_size: int
