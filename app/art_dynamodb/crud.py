from pynamodb.exceptions import DoesNotExist, DeleteError, GetError, ScanError, QueryError, TableError, TableDoesNotExist
from . import schemas, models
import datetime
from uuid import uuid4

# -----------------------
# DynamoDB CRUD functions
# -----------------------


async def get_all_base_layers(rate_limit: int = 15) -> list[schemas.Layer]:
    try:
        layer_list = []
        for layer in models.Layer.scan(models.Layer.is_base_layer == True, rate_limit=rate_limit):  # Rate limit(RCU per second)
            layer_list.append(schemas.Layer(**layer.attribute_values))
        return layer_list
    except ScanError as error:
        raise error
    except Exception as error:
        raise error


async def get_all_created_layers(rate_limit: int = 15) -> list[schemas.Layer]:
    try:
        layer_list = []
        for layer in models.Layer.scan(models.Layer.is_base_layer == False, rate_limit=rate_limit):  # Rate limit(RCU per second)
            layer_list.append(schemas.Layer(**layer.attribute_values))
        return layer_list
    except Exception as error:
        raise error


async def create_layer(schema: schemas.LayerCreate) -> schemas.Layer:
    try:
        models.Layer.create_table(read_capacity_units=1, write_capacity_units=1)
    except Exception as error:
        raise error

    generated_id = str(uuid4())
    current_datetime = datetime.datetime.now()
    is_base_layer = False if schema.base_layer_id else True
    base_layer_id = schema.base_layer_id if schema.base_layer_id else generated_id

    layer = models.Layer(
        id=generated_id,
        base_layer_id=base_layer_id,
        owner_id=schema.owner_id,
        art_name=schema.art_name,
        artist_name=schema.artist_name,
        file_name=schema.file_name,
        height=schema.height,
        width=schema.width,
        is_base_layer=is_base_layer,
        created_at=current_datetime
    )

    try:
        layer.save()
        return schemas.Layer(**layer.attribute_values)
    except Exception as error:
        raise error


async def get_artwork(layer_id: str) -> schemas.Artwork:
    try:
        top_layer = models.Layer.query(layer_id).next()
    except DoesNotExist as error:
        raise error
    except Exception as error:
        raise error

    try:
        result = models.Layer.scan((models.Layer.base_layer_id == top_layer.base_layer_id) & (models.Layer.created_at <= top_layer.created_at))
    except Exception as error:
        raise error

    layer_list = []
    for layer in result:
        layer_list.append(layer)

    sorted_layer_list = []
    for layer in sorted(layer_list, key=lambda x: x.created_at, reverse=True):
        sorted_layer_list.append(schemas.Layer(**layer.attribute_values))

    return schemas.Artwork(layers=sorted_layer_list, **top_layer.attribute_values)


async def delete_layer(layer_id: str, created_at: datetime.datetime) -> schemas.Layer:
    try:
        layer = models.Layer.get(hash_key=layer_id, range_key=created_at)
    except DoesNotExist as error:
        raise error
    except Exception as error:
        raise error

    try:
        layer.delete()
    except DeleteError as error:
        raise error
    except Exception as error:
        raise error

    return schemas.Layer(**layer.attribute_values)


async def get_artwork_history(layer_id: str) -> list[schemas.Artwork]:
    try:
        top_layer = models.Layer.query(layer_id).next()
    except QueryError as error:
        raise error
    except Exception as error:
        raise error

    try:
        result = models.Layer.scan(models.Layer.base_layer_id == top_layer.base_layer_id)
    except Exception as error:
        raise error

    layer_list = []
    for layer in result:
        layer_list.append(layer)

    artwork_list = []
    for layer in sorted(layer_list, key=lambda x: x.created_at, reverse=True):
        try:
            artwork_list.append(await get_artwork(layer.id))
        except Exception as error:
            raise error

    return artwork_list


async def get_latest_artworks() -> list[schemas.Artwork]:
    try:
        result = models.Layer.scan(models.Layer.is_base_layer == True)
    except Exception as error:
        raise error

    artwork_list = []
    for base_layer in result:
        try:
            # Get all layers that share the base_layer_id
            result = models.Layer.scan(models.Layer.base_layer_id == base_layer.id)
        except Exception as error:
            raise error

        layer_list = []
        for layer in result:
            layer_list.append(layer)

        # Add base layer to layer list
        layer_list.append(base_layer)

        # Sort layer list by timestamp and return a "schema layer" list
        sorted_layer_list = []
        for layer in sorted(layer_list, key=lambda x: x.created_at, reverse=True):
            sorted_layer_list.append(schemas.Layer(**layer.attribute_values))

        # Create artwork from base layer and (sorted) layer list then append to artwork list
        artwork_list.append(schemas.Artwork(layers=sorted_layer_list, **sorted_layer_list[0].dict()))

    return artwork_list


async def set_artwork_active(layer_id: str, is_active: bool) -> schemas.Layer:
    try:
        layer = models.Layer.query(layer_id).next()
    except DoesNotExist as error:
        raise error
    except Exception as error:
        raise error

    if layer.is_active == is_active:
        return schemas.Layer(**layer.attribute_values)

    try:
        layer.is_active = is_active
        layer.save()
    except Exception as error:
        raise error

    return schemas.Layer(**layer.attribute_values)
