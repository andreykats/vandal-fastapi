from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute

from ..db_dynamo import config

import sys


class BaseTable(Model):
    class Meta:
        host = config.DB_HOST if config.ENVIRONMENT in ["local", "test"] else None
        region = config.AWS_REGION if config.ENVIRONMENT in ["test"] else None
        aws_access_key_id = config.AWS_ACCESS_KEY_ID if config.ENVIRONMENT in ["test"] else None


class MessageTable(BaseTable):
    class Meta(BaseTable.Meta):
        table_name = "websocket-history-table"
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute()
    channel = UnicodeAttribute(hash_key=True)
    body = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(range_key=True)


# Create the table
try:
    if not MessageTable.exists():
        MessageTable.create_table(wait=True)
except Exception as e:
    print("Database not available.")
