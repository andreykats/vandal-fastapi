from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, KeysOnlyProjection

from ..db_dynamo import config


class BaseTable(Model):
    class Meta:
        host = config.DB_HOST
        region = config.AWS_REGION
        aws_access_key_id = config.AWS_ACCESS_KEY_ID

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


class LayerTable(BaseTable):
    class Meta(BaseTable.Meta):
        table_name = "layer-table"
        read_capacity_units = 1
        write_capacity_units = 1

    id = UnicodeAttribute(hash_key=True)
    base_layer_id = UnicodeAttribute(null=True)
    layer_type = UnicodeAttribute(default="created")
    owner_id = UnicodeAttribute(default="1")
    art_name = UnicodeAttribute()
    artist_name = UnicodeAttribute()
    file_name = UnicodeAttribute(null=True)
    width = NumberAttribute()
    height = NumberAttribute()
    is_active = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(range_key=True)

    base_layer_id_index = BaseLayerIdIndex()
    layer_type_index = LayerTypeIndex()


# Create the table
try:
    if not LayerTable.exists():
        LayerTable.create_table(wait=True)
except Exception as e:
    print("Database not available.")
