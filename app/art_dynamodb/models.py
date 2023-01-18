from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


class Layer(Model):
    """
    A DynamoDB Layer
    """
    class Meta:
        table_name = "layers"
        host = "http://localhost:8000"
        aws_access_key_id = 'AKIAVMXD3KUKQJMIJDSZ'
        # aws_secret_access_key = 'AKIAVMXD3KUKQJMIJDSZ'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    owner_id = NumberAttribute(default=0)
    base_layer_id = UnicodeAttribute()
    created_at = UTCDateTimeAttribute()
