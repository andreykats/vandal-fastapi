# from pydantic import BaseModel
# from ..art.schemas import Item


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True
