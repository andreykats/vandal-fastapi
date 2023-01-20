from pydantic import BaseModel, Field
from pydantic.schema import Optional


class ItemBase(BaseModel):
    name: str = Field(example="Mona Lisa")
    owner_id: int = Field(example=1)
    base_layer_id: Optional[int] = Field(example=4)
    height: int = Field(example=100)
    width: int = Field(example=100)


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Artwork(BaseModel):
    id: int
    name: str
    is_active: bool
    height: int
    width: int
    layers: list[Item]
