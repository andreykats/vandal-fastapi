from pydantic import BaseModel, Field
from pydantic.schema import Optional
from datetime import datetime


class MessageBase(BaseModel):
    channel: str = Field(example="1")
    body: str = Field(example="Lorem ipsum")


class MessageCreate(MessageBase):
    pass


class Layer(MessageBase):
    id: str
    created_at: datetime
