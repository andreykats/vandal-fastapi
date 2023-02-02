from aws_lambda_powertools.utilities.typing import LambdaContext
from os import environ
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

############################################################################################################
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
############################################################################################################

BROADCAST_CHANNEL = '0'
connections_table = boto3.resource('dynamodb').Table(environ.get('TABLE_NAME'))

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

    messages = body.get('payload', {}).get('messages')
    if not messages:
        logger.exception("Missing messages")
        return {'statusCode': 400, 'body': 'Missing messages'}

    # Get all connections for channel
    try:
        response = connections_table.query(IndexName='channel_id_index',KeyConditionExpression=Key('channel_id').eq(channel_id))
    except ClientError:
        logger.exception("Failed query connections table.")
        return {'statusCode': 500, 'body': 'Failed query connections table'}

    connection_id_list = [item['connection_id'] for item in response['Items']]
    logger.info("Found %s active connections.", len(connection_id_list))

    # Setup websocket messaging client
    client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain_name}/{stage_name}')

    # Send message to all connections
    for connection_id in connection_id_list:
        for message in messages:
            body = {}
            body["action"] = "sendmessage"
            body["payload"] = {}
            body["payload"]["channel"] = channel_id
            body["payload"]["message"] = message["body"]

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

    return {'statusCode': 200, 'body': 'Data sent'}