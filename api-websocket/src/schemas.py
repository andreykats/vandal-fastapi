from aws_lambda_powertools.utilities.parser import BaseModel

class Message(BaseModel):
    id: str
    channel: str
    body: str
    created_at: str

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