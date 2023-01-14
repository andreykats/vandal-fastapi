from pydantic import BaseModel, Field
from pydantic.schema import Optional


class ItemBase(BaseModel):
    name: str = Field(example="Mona Lisa")
    owner_id: int = Field(example=1)
    base_layer_id: Optional[int] = Field(example=4)


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class Artwork(BaseModel):
    id: int
    name: str
    layers: list[Item]
