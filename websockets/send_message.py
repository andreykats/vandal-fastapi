from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from os import environ
import json
import logging
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger()
logger.setLevel(logging.INFO)

############################################################################################################
# body: {
#     "action":"sendmessage", 
#     "payload":  {
#         "channel": "0",
#         "message": "Lorem ipsum"
#     }
# }  
############################################################################################################

BROADCAST_CHANNEL = '0'
connections_table = boto3.resource('dynamodb').Table(environ.get('TABLE_NAME'))
messages_table = boto3.resource('dynamodb').Table(environ.get('DB_TABLE_MESSAGES'))

def handler(event: dict, context: LambdaContext) -> dict:
    # logger.info(f"Event: {event}")
    domain_name = event.get('requestContext', {}).get('domainName')
    stage_name = event.get('requestContext', {}).get('stage')

    body = json.loads(event.get('body', None))
    if not body:
        logger.exception("Missing body")
        return {'statusCode': 400, 'body': 'Missing body'}

    channel_id = body.get('payload', {}).get('channel')
    if not channel_id:
        logger.exception("Missing channel")
        return {'statusCode': 400, 'body': 'Missing channel'}

    message = body.get('payload', {}).get('message')
    if not message:
        logger.exception("Missing message")
        return {'statusCode': 400, 'body': 'Missing message'}

    # Get all connections for channel
    try:
        response = connections_table.query(IndexName='channel_id_index',KeyConditionExpression=Key('channel_id').eq(channel_id))
    except ClientError:
        logger.exception("Couldn't get connections.")
        return {'statusCode': 500, 'body': 'Failed query connections table'}

    connection_id_list = [item['connection_id'] for item in response['Items']]
    logger.info("Found %s active connections.", len(connection_id_list))

    # Setup websocket messaging client
    client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain_name}/{stage_name}')

    # Send message to all connections
    for connection_id in connection_id_list:
        try:
            client.post_to_connection(ConnectionId=connection_id, Data=json.dumps(body))
            logger.info(f"Posted message: {body} to connection_id: {connection_id}")
        except client.exceptions.GoneException:
            logger.info("Connection %s is gone, removing.", connection_id)
            try:
                connections_table.delete_item(Key={'connection_id': connection_id})
                logger.info("Removed connection: %s.", connection_id)
            except ClientError:
                logger.exception("Could not remove connection: %s.", connection_id)
                continue
        except ClientError as error:
            logger.exception("Couldn't post to connection %s.", connection_id)
            continue

    # Do not save message if sent to broadcast channel
    if channel_id == BROADCAST_CHANNEL:
        return {'statusCode': 200, 'body': 'Data sent'}

    # Save message to database
    try:
        item = {
            "id": str(uuid4()),
            'channel': channel_id, 
            'body': message, 
            'created_at': datetime.now().isoformat()
        }

        messages_table.put_item(Item=item)
        logger.info(f"Saved message: {item}")
    except Exception as error:
        logger.exception("Problem saving message: %s", error)
        return {'statusCode': 500, 'body': 'Failed to save message'}

    return {'statusCode': 200, 'body': 'Data sent and saved'}


