from pydantic import BaseModel
from pydantic.schema import Optional


class ItemBase(BaseModel):
    name: str
    url: str
    parent_id: Optional[int]
    owner_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
