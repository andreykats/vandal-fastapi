from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


class CreatedAtIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'created-at-index'
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    created_at = UTCDateTimeAttribute(hash_key=True)


# class BaseLayer(Model):
#     class Meta:
#         table_name = "base-layers"
#         host = "http://localhost:8000"
#         aws_access_key_id = 'AKIAVMXD3KUKQJMIJDSZ'
#         # aws_secret_access_key = 'AKIAVMXD3KUKQJMIJDSZ'

#     id = UnicodeAttribute(hash_key=True)
#     owner_id = UnicodeAttribute(default=1)
#     art_name = UnicodeAttribute(range_key=True)
#     artist_name = UnicodeAttribute()
#     width = NumberAttribute()
#     height = NumberAttribute()
#     created_at = UTCDateTimeAttribute()


class Layer(Model):
    class Meta:
        table_name = "artwork-layers"
        host = "http://localhost:8000"
        aws_access_key_id = 'AKIAVMXD3KUKQJMIJDSZ'

    id = UnicodeAttribute(hash_key=True)
    base_layer_id = UnicodeAttribute()
    owner_id = UnicodeAttribute(default=1)
    art_name = UnicodeAttribute()
    artist_name = UnicodeAttribute()
    file_name = UnicodeAttribute()
    width = NumberAttribute()
    height = NumberAttribute()
    is_base_layer = BooleanAttribute()
    is_active = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(range_key=True)
