from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute

from ..config import config


class BaseTable(Model):
    class Meta:
        host = config.DB_HOST
        region = config.AWS_REGION
        aws_access_key_id = config.AWS_ACCESS_KEY_ID


class MessageTable(BaseTable):
    class Meta(BaseTable.Meta):
        table_name = config.DB_TABLE_MESSAGES
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute()
    channel = UnicodeAttribute(hash_key=True)
    body = UnicodeAttribute()
    # created_at = UTCDateTimeAttribute(range_key=True)
    created_at = UnicodeAttribute(range_key=True)


# Create the table
try:
    if not MessageTable.exists():
        MessageTable.create_table(wait=True)
except Exception as e:
    print("Database not available.")
