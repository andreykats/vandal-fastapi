from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import environ
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import json
import logging

from . import schemas

logger = logging.getLogger()
logger.setLevel(logging.INFO)

connections_table = boto3.resource('dynamodb').Table(environ.get('DB_TABLE_CONNECTIONS'))
messages_table = boto3.resource('dynamodb').Table(environ.get('DB_TABLE_MESSAGES'))
client = boto3.client('lambda')

SEND_MESSAGE_FUNCTION = "VANDAL-Stage-sendMessageFunction"
BULK_SEND_MESSAGE_FUNCTION = "VANDAL-Stage-bulkSendMessageFunction"

def handler(event: dict, context: LambdaContext) -> dict:
    # logger.info(f"Event: {event}")
    channel_id: str = event.get('queryStringParameters', {'channel': '0'}).get('channel')
    connection_id: str = event.get('requestContext', {}).get('connectionId')

    try:
        connections_table.put_item(Item={'connection_id': connection_id, 'channel_id': channel_id})
        logger.info(f"Added connection_id: {connection_id} for channel_id: {channel_id}")
    except ClientError:
        logger.exception(f"Couldn't add connection_id: {connection_id} for channel_id: {channel_id}")
        return {'statusCode': 503, 'body': 'Failed to connect : '}
    
    send_welcome_message(channel_id=channel_id, connection_id=connection_id, event=event)
    send_message_history(channel_id=channel_id, event=event)

    return {'statusCode': 200, 'body': 'Connected'}


def send_welcome_message(channel_id: str, connection_id: str, event: dict):
    welcome_msg = schemas.Body(
        payload=schemas.SinglePayload(
            channel=channel_id, 
            message=schemas.Message(
                body=f"Welcome, {connection_id}!"
            )
        )
    )
    outgoing_event = event
    outgoing_event["body"] = json.dumps(welcome_msg.dict())

    try:
        client.invoke(FunctionName=SEND_MESSAGE_FUNCTION, InvocationType='Event', Payload=json.dumps(outgoing_event))
    except Exception as error:
        logger.exception(f"Couldn't invoke {SEND_MESSAGE_FUNCTION}. Error: {error}")
        raise error

    return True

def send_message_history(channel_id: str, event: dict):
    try:
        response = messages_table.query(KeyConditionExpression=Key('channel').eq(channel_id))
        # logger.info(f"Query response: {response['Items']}")
    except ClientError:
        logger.exception("Couldn not query messeges table")
        raise ClientError

    # body: {
    #     "action":"bulksendmessage", 
    #     "payload":  {
    #         "channel": "0",
    #         "messages": [
    #               {"body": "Lorem ipsum", "created_at": "123"},
    #               {"body": "Lorem ipsum", "created_at": "123"}    
    #         ]
    #     }
    # }  

    # body = {}
    # body["action"] = "bulksendmessage"
    # body["payload"] = {}
    # body["payload"]["channel"] = channel_id
    # body["payload"]["messages"] = sorted(response['Items'], key=lambda msg: msg["created_at"])

    message_history = schemas.BulkBody(
        payload=schemas.BulkPayload(
            channel=channel_id, 
            messages=sorted(response['Items'], key=lambda msg: msg["created_at"])
        )
    )
    
    # Replace event body with new body
    outgoing_event = event
    outgoing_event["body"] = json.dumps(message_history.dict())
    # event["body"] = json.dumps(body)
    
    try:
        client.invoke(FunctionName=BULK_SEND_MESSAGE_FUNCTION, InvocationType='Event', Payload=json.dumps(outgoing_event))
    except Exception as error:
        logger.exception(f"Couldn't invoke {BULK_SEND_MESSAGE_FUNCTION}. Error: {error}")
        raise error
        
    return True