from . import models
from . import schemas
from uuid import uuid4
from datetime import datetime

# -----------------------
# DynamoDB CRUD functions
# -----------------------


async def get_messages(channel: str) -> list[schemas.Message]:
    try:
        result = models.MessageTable.query(channel)
    except Exception as error:
        raise error

    message_list = []
    for model in result:
        message_list.append(schemas.Message(**model.attribute_values))

    # return list sorted by created_at
    return sorted(message_list, key=lambda msg: msg.created_at)


async def create_message(message: schemas.MessageCreate) -> models.MessageTable:
    model = models.MessageTable(
        id=str(uuid4()),
        channel=message.channel,
        body=message.body,
        created_at=datetime.now()
    )

    try:
        model.save()
        return model
    except Exception as error:
        raise error


async def delete_channel_history(channel: str) -> dict:
    try:
        result = models.MessageTable.query(channel)
    except Exception as error:
        raise error

    result_list = []
    for model in result:
        try:
            result_list.append(model.delete())
        except Exception as error:
            raise error

    return {"messages_deleted": len(result_list)}
