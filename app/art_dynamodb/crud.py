from pynamodb.exceptions import DoesNotExist, DeleteError, GetError, ScanError, QueryError, TableError, TableDoesNotExist
from . import schemas, models
import datetime
from uuid import uuid4
from enum import Enum

# -----------------------
# DynamoDB CRUD functions
# -----------------------


CREATED_LAYER = "CREATED"
BASE_LAYER = "BASE"


async def get_all_base_layers(rate_limit: int = 15) -> list[schemas.LayerSchema]:
    try:
        layer_list = []
        for layer in models.LayerTable.scan(models.LayerTable.layer_type == BASE_LAYER, rate_limit=rate_limit):  # Rate limit(RCU per second)
            layer_list.append(schemas.LayerSchema(**layer.attribute_values))
        return layer_list
    except ScanError as error:
        raise error
    except Exception as error:
        raise error


async def get_all_created_layers(rate_limit: int = 15) -> list[schemas.LayerSchema]:
    try:
        layer_list = []
        for layer in models.LayerTable.scan(models.LayerTable.layer_type == CREATED_LAYER, rate_limit=rate_limit):  # Rate limit(RCU per second)
            layer_list.append(schemas.LayerSchema(**layer.attribute_values))
        return layer_list
    except ScanError as error:
        raise error
    except Exception as error:
        raise error


async def create_layer(schema: schemas.LayerCreateSchema) -> models.LayerTable:
    generated_id = str(uuid4())
    current_datetime = datetime.datetime.now()
    layer_type = CREATED_LAYER if schema.base_layer_id else BASE_LAYER
    base_layer_id = schema.base_layer_id if schema.base_layer_id else generated_id

    model = models.LayerTable(
        id=generated_id,
        base_layer_id=base_layer_id,
        owner_id=schema.owner_id,
        art_name=schema.art_name,
        artist_name=schema.artist_name,
        file_name=schema.file_name,
        height=schema.height,
        width=schema.width,
        layer_type=layer_type,
        created_at=current_datetime
    )

    try:
        model.save()
        return model
    except Exception as error:
        raise error


# 1 Query
async def get_artwork_from_layer(layer: models.LayerTable) -> schemas.ArtworkSchema:
    try:
        # Get all layers that share the found Layer's base_layer_id
        result = models.LayerTable.base_layer_id_index.query(layer.base_layer_id, models.LayerTable.created_at <= layer.created_at)
    except Exception as error:
        raise error

    layer_list = []
    for each in result:
        layer_list.append(models.LayerTable(**each.attribute_values))

    sorted_layer_list = []
    for sorted_layer in sorted(layer_list, key=lambda x: x.created_at, reverse=True):
        sorted_layer_list.append(schemas.LayerSchema(**sorted_layer.attribute_values))

    return schemas.ArtworkSchema(layers=sorted_layer_list, **layer.attribute_values)


# 2 Queries
async def get_artwork_from_id(layer_id: str) -> schemas.ArtworkSchema:
    try:
        # Get the Layer for the given layer_id
        top_layer = models.LayerTable.query(layer_id).next()
    except DoesNotExist as error:
        raise error
    except Exception as error:
        raise error

    try:
        return await get_artwork_from_layer(layer=top_layer)
    except Exception as error:
        raise error


# 1 Query
async def delete_layer(layer_id: str) -> schemas.LayerSchema:
    try:
        layer = models.LayerTable.query(layer_id).next()
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

    return schemas.LayerSchema(**layer.attribute_values)


# Largest offender of queries
async def get_artwork_history(layer_id: str) -> list[schemas.ArtworkSchema]:
    try:
        top_layer = models.LayerTable.query(layer_id).next()
    except QueryError as error:
        raise error
    except Exception as error:
        raise error

    try:
        result = models.LayerTable.base_layer_id_index.query(top_layer.base_layer_id)
    except Exception as error:
        raise error

    layer_list = []
    for layer in result:
        layer_list.append(layer)

    artwork_list = []
    for layer in sorted(layer_list, key=lambda x: x.created_at, reverse=True):
        try:
            artwork_list.append(await get_artwork_from_layer(layer=layer))
        except Exception as error:
            raise error

    return artwork_list


# 1 + 1 Queries per artwork
async def get_latest_artworks() -> list[schemas.ArtworkSchema]:
    try:
        # Get all base layers
        result = models.LayerTable.layer_type_index.query(BASE_LAYER)
    except Exception as error:
        raise error

    artwork_list = []
    for base_layer in result:
        try:
            # Get all layers that share the base_layer_id
            result = models.LayerTable.base_layer_id_index.query(base_layer.id)
        except Exception as error:
            raise error

        layer_list = []
        for layer in result:
            layer_list.append(layer)

        # Add base layer to layer list
        # layer_list.append(base_layer)

        # Sort layer list by timestamp and return a "schema layer" list
        sorted_layer_list = []
        for layer in sorted(layer_list, key=lambda x: x.created_at, reverse=True):
            sorted_layer_list.append(schemas.LayerSchema(**layer.attribute_values))

        # Create artwork from base layer and (sorted) layer list then append to artwork list
        artwork_list.append(schemas.ArtworkSchema(layers=sorted_layer_list, **sorted_layer_list[0].dict()))

    print(len(artwork_list))
    return artwork_list


# async def set_artwork_active(layer_id: str, is_active: bool) -> schemas.Artwork:
#     try:
#         layer = models.LayerTable.query(layer_id).next()
#     except DoesNotExist as error:
#         raise error
#     except Exception as error:
#         raise error

#     if layer.is_active == is_active:
#         return schemas.Layer(**layer.attribute_values)

#     try:
#         layer.is_active = is_active
#         layer.save()
#     except Exception as error:
#         raise error

#     try:
#         artwork = await get_artwork_from_layer(layer=layer)
#     except Exception as error:
#         raise error

#     return artwork


async def set_layer_active(layer_id: str, is_active: bool) -> models.LayerTable:
    try:
        layer = models.LayerTable.query(layer_id).next()
    except DoesNotExist as error:
        raise error
    except Exception as error:
        raise error

    if layer.is_active == is_active:
        # return schemas.Layer(**layer.attribute_values)
        return layer

    try:
        layer.is_active = is_active
        layer.save()
    except Exception as error:
        raise error

    return layer
