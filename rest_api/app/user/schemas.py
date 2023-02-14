from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    cognito_id: str
    is_active: bool
    is_superuser: bool
    created_at: datetime