from . import schemas, models
from uuid import uuid4
from datetime import datetime
import json

# -----------------------
# DynamoDB CRUD functions
# -----------------------


def get_messages(channel: str) -> list[models.Message]:
    if not models.Message.exists():
        models.Message.create_table(read_capacity_units=1, write_capacity_units=1)

    message_list = []
    for layer in models.Message.query(channel):
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


async def delete_channel_history(channel: str) -> json:
    try:
        result = models.Message.query(channel)
    except Exception as error:
        raise error

    result_list = []
    for message in result:
        try:
            result_list.append(message.delete())
        except Exception as error:
            raise error

    return {"messages_deleted": len(result_list)}
