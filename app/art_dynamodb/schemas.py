from pydantic import BaseModel, Field
from pydantic.schema import Optional
from datetime import datetime
from uuid import UUID


class LayerBase(BaseModel):
    name: str = Field(example="Mona Lisa")
    owner_id: int = Field(example=1)
    base_layer_id: Optional[str] = Field(example="1")


class LayerCreate(LayerBase):
    pass


class Layer(LayerBase):
    id: str
    created_at: datetime


class Artwork(BaseModel):
    id: int
    name: str
    layers: list[Layer]
