import boto3
from boto3.resources.base import ServiceResource


def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://localhost:8000',
                         region_name='us-east-1',
                         aws_access_key_id='example',
                         aws_secret_access_key='AKIAVMXD3KUKQJMIJDSZ')
    return ddb


def generate_table(ddb):
    ddb.create_table(
        TableName='Layers',                # create table
        AttributeDefinitions=[
            {
                'AttributeName': 'uid',     # In this case, I only specified uid as partition key (there is no sort key)
                'AttributeType': 'S'        # with type string
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'uid',     # attribute uid serves as partition key
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={             # specying read and write capacity units
            'ReadCapacityUnits': 10,        # these two values really depend on the app's traffic
            'WriteCapacityUnits': 10
        }
    )
    print('Successfully created table')


Service = initialize_db()

# if __name__ == "__main__":
#     generate_table(initialize_db())
