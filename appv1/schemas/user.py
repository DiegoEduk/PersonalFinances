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

class UserLoggin(UserBase):
    user_id: str

class PermissionsRol(BaseModel):
    module_name: str
    p_select: bool

class ResponseLoggin(BaseModel):
    user: UserLoggin
    permissions: List[PermissionsRol]
    access_token: str

    
   # token api mailsend
   # mlsn.4b0e930b61ef65f5cb7ecf27123c0a30ca9c02b185b3c31e97596a5a67feff0e
   # mlsn.1c6857b7db7c6cb3155af4607e0ccae43c62007dddd3bc2fec2d90c86fd126f8