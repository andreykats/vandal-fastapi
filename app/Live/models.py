from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


class Message(Model):
    """
    A DynamoDB Layer
    """
    class Meta:
        table_name = "websocket-history"
        host = "http://localhost:8000"
        aws_access_key_id = 'AKIAVMXD3KUKQJMIJDSZ'
        # aws_secret_access_key = 'AKIAVMXD3KUKQJMIJDSZ'

    id = UnicodeAttribute()
    channel = UnicodeAttribute(hash_key=True)
    body = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(range_key=True)


# class Channel(Model):
#     """
#     A DynamoDB Layer
#     """
#     class Meta:
#         table_name = "websocket-history"
#         host = "http://localhost:8000"
#         aws_access_key_id = 'AKIAVMXD3KUKQJMIJDSZ'
#         # aws_secret_access_key = 'AKIAVMXD3KUKQJMIJDSZ'

#     id = UnicodeAttribute(hash_key=True)
#     messages = ListAttribute(of=Message)
#     created_at = UTCDateTimeAttribute()
