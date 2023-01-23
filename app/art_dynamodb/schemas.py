from pydantic import BaseModel, Field
from pydantic.schema import Optional
from datetime import datetime


class LayerBase(BaseModel):
    base_layer_id: Optional[str] = Field(example="pf08ag12-g8c7-4e0b-hr5d-hd6c88ce8b92")
    owner_id: str = Field(example="da09a712-d5c7-4e0b-be5d-2d6c98ce8b92")
    art_name: str = Field(example="Mona Lisa")
    artist_name: str = Field(example="Leonardo Da Vinci")
    file_name: Optional[str] = Field(example="mona-lisa.png")
    width: int = Field(example=100)
    height: int = Field(example=100)


class LayerCreate(LayerBase):
    pass


class Layer(LayerBase):
    id: str
    is_active: bool
    created_at: datetime


class Artwork(BaseModel):
    owner_id: str
    art_name: str
    artist_name: str
    height: int
    width: int
    is_active: bool
    layers: list[Layer]
    created_at: datetime
