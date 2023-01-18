from . import schemas, models
from uuid import uuid4
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource


def get_all_items(rate_limit: int = 15):
    # Rate limit(RCU per second)
    layer_list = []
    for layer in models.Layer.scan(models.Layer.created_at.between(datetime(2021, 1, 1), datetime.now()), rate_limit=rate_limit):
        layer_list.append(layer.attribute_values)

    return layer_list


def create_item(item: schemas.LayerCreate):
    print(models.Layer.create_table(read_capacity_units=1, write_capacity_units=1))
    generated_id = str(uuid4())
    db_item = models.Layer(
        id=generated_id,
        name=item.name,
        owner_id=item.owner_id,
        base_layer_id=(item.base_layer_id if item.base_layer_id != None else generated_id),
        created_at=datetime.now()
    )

    db_item.save()
    return db_item.attribute_values


# def get_feed_items():
    # Get all base_layer_ids
    # unique_base_layer_ids = set()
    # for layer in models.BaseLayer.scan(models.Layer.created_at.between(datetime(2021, 1, 1), datetime.now())):
    #    layer_dict = layer.attribute_values
    #    layer_list.append(layer_dict['base_layer_id'])

    # For every base_id add the most recent layer created
    # artwork_list = []
    # for id in unique_base_layer_ids:
    # item = models.Layer.get(id)
    # items = models.Layer.scan(models.Layer.base_layer_id == item.id)
    # artwork_list.append(schemas.Artwork(id=item.id, name=item.name, layers=items))

    # Sort by most recent submissions
    # sorted_feed = sorted(feed, key=lambda x: x.id, reverse=True)

    # return artwork_list
    # return sorted_feed
