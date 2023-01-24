from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, KeysOnlyProjection


class BaseLayerIdIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        index_name = 'base_layer_id_index'
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    base_layer_id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute(range_key=True)


class LayerTypeIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'layer_type_index'
        read_capacity_units = 2
        write_capacity_units = 1
        projection = KeysOnlyProjection()

    layer_type = UnicodeAttribute(default="created", hash_key=True)


class Layer(Model):
    class Meta:
        table_name = "art-layers"
        host = "http://localhost:8000"
        aws_access_key_id = 'AKIAVMXD3KUKQJMIJDSZ'

    id = UnicodeAttribute(hash_key=True)
    base_layer_id_index = BaseLayerIdIndex()
    base_layer_id = UnicodeAttribute()
    layer_type_index = LayerTypeIndex()
    layer_type = UnicodeAttribute(default="created")
    owner_id = UnicodeAttribute(default=1)
    art_name = UnicodeAttribute()
    artist_name = UnicodeAttribute()
    file_name = UnicodeAttribute(null=True)
    width = NumberAttribute()
    height = NumberAttribute()
    is_active = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(range_key=True)
