from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, KeysOnlyProjection
from ..config import config

class BaseTable(Model):
    class Meta:
        host = config.DB_HOST
        region = config.AWS_REGION
        aws_access_key_id = config.AWS_ACCESS_KEY_ID

class UsersTable(BaseTable):
    class Meta(BaseTable.Meta):
        table_name = config.DB_TABLE_USERS
        read_capacity_units = 1
        write_capacity_units = 1

    email = UnicodeAttribute(hash_key=True)
    cognito_id = UnicodeAttribute(null=False)
    is_active = BooleanAttribute(default=False)
    is_superuser = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(range_key=True)

# Create the table
try:
    if not UsersTable.exists():
        UsersTable.create_table(wait=True)
except Exception as e:
    print("Database not available.")
