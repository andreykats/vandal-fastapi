from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    url: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    parent_id: int
    owner_id: int

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
