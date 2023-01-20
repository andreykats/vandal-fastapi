from . import schemas, models
from uuid import uuid4
from datetime import datetime
import json

from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource


def get_messages(channel: str) -> list[models.Message]:
    if not models.Message.exists():
        models.Message.create_table(read_capacity_units=1, write_capacity_units=1)

    message_list = []
    for layer in models.Message.scan(models.Message.channel == channel):
        message_list.append(layer.attribute_values)

    # return list sorted by created_at
    return sorted(message_list, key=lambda k: k['created_at'])


def create_message(message: schemas.MessageCreate) -> models.Message:
    if not models.Message.exists():
        models.Message.create_table(read_capacity_units=1, write_capacity_units=1)

    message = models.Message(
        id=str(uuid4()),
        channel=message.channel,
        body=message.body,
        created_at=datetime.now()
    )
    message.save()

    return message.attribute_values


def delete_messages(channel: str) -> json:
    result_list = []
    for message in models.Message.scan(models.Message.channel == channel):
        result_list.append(message.delete())
    return json.dumps({"messages_deleted": len(result_list)})
