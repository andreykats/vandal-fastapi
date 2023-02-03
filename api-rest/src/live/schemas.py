from pydantic import BaseModel, Field
from pydantic.schema import Optional
from datetime import datetime


class MessageBase(BaseModel):
    channel: str = Field(example="1")
    body: str = Field(example="Lorem ipsum")


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: str = Field(example="da09a712-d5c7-4e0b-be5d-2d6c98ce8b92")
    created_at: datetime
