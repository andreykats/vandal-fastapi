from aws_lambda_powertools.utilities.parser import BaseModel
from pydantic.schema import Optional

class Message(BaseModel):
    id: Optional[str]
    channel: Optional[str]
    body: str
    created_at: Optional[str]

class Payload(BaseModel):
    channel: str

class SinglePayload(Payload):
    message: Message

class BulkPayload(Payload):
    messages: list[Message]

class Body(BaseModel):
    action: str = "sendmessage"
    payload: SinglePayload

class BulkBody(BaseModel):
    action: str = "bulksendmessage"
    payload: BulkPayload