from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import environ
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

table = boto3.resource('dynamodb').Table(environ.get('TABLE_NAME'))

def handler(event: dict, context: LambdaContext) -> dict:
    connection_id = event.get('requestContext', {}).get('connectionId')

    try:
        table.delete_item(Key={'connection_id': connection_id})
    except Exception as error:
        return {'statusCode': 500, 'body': 'Failed to disconnect: ' + str(error)}

    return {'statusCode': 200, 'body': 'Connected'}