from pydantic import BaseModel, Field
from pydantic.schema import Optional
import json


class ItemBase(BaseModel):
    name: str = Field(example="Mona Lisa")
    owner_id: int = Field(example=1)
    base_layer_id: Optional[int] = Field(example=4)


class ItemCreate(ItemBase):
    pass

    # Below validators make it possible to use UploadFile and Pydantic model in the same request
    # https://github.com/tiangolo/fastapi/issues/2257
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


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
