from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import environ
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import json
import logging

import schemas

logger = logging.getLogger()
logger.setLevel(logging.INFO)

connections_table = boto3.resource('dynamodb').Table(environ.get('TABLE_NAME'))
messages_table = boto3.resource('dynamodb').Table(environ.get('DB_TABLE_MESSAGES'))

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

    try:
        response = messages_table.query(KeyConditionExpression=Key('channel').eq(channel_id))
        # logger.info(f"Query response: {response['Items']}")
    except ClientError:
        logger.exception("Couldn not query messeges table")
        return {'statusCode': 404, 'body': "Couldn not query messeges table" }   

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

    body = schemas.BulkBody(
        payload=schemas.BulkPayload(
            channel=channel_id, 
            messages=sorted(response['Items'], key=lambda msg: msg["created_at"])
        )
    )
    
    # Replace event body with new body
    event["body"] = json.dumps(body.dict())
    # event["body"] = json.dumps(body)
    
    client = boto3.client('lambda')
    try:
        client.invoke(FunctionName='BulkSendMessageFunction', InvocationType='Event', Payload=json.dumps(event))
    except Exception as error:
        logger.exception(f"Couldn't invoke SendMessageFunction. Error: {error}")
        return {'statusCode': 500, 'body': 'Failed to send message '}
        
    return {'statusCode': 200, 'body': 'Connected'}