# from typing import List
# from sqlalchemy.orm import Session
# from sqlalchemy import select
# from . import models, schemas
# from ..live import crud


# def get_all_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
#     return db.query(models.Item).offset(skip).limit(limit).all()


# async def get_item(db: Session, item_id: int) -> models.Item:
#     return await db.query(models.Item).filter(models.Item.id == item_id).first()


# async def set_item_active(db: Session, item_id: int, is_active: bool) -> models.Item:
#     item = await get_item(db, item_id=item_id)
#     if item.is_active == is_active:
#         return item

#     # Delete all messages from DynamoDB if item is beinxzsaabvcvbnvvnmbg deactivated
#     if item.is_active == True and is_active == False:
#         await crud.delete_channel_history(channel=item.name)

#     item.is_active = is_active
#     db.commit()
#     db.refresh(item)

#     return item


# def get_feed_items(db: Session) -> List[schemas.Artwork]:
#     # Get all base_layer_ids and flatten to remove tuple
#     all_base_layer_ids = [id for id, in db.execute(select(models.Item.base_layer_id))]

#     # Return unique
#     unique_base_layer_ids = set(all_base_layer_ids)

#     # Create a new feed array
#     artwork_list = []

#     # For every base_id add the most recent layer created
#     for id in unique_base_layer_ids:
#         item = db.query(models.Item).filter(models.Item.base_layer_id == id).order_by(models.Item.id.desc()).first()
#         items = db.query(models.Item).filter(models.Item.base_layer_id == id).order_by(models.Item.id.desc()).all()
#         artwork_list.append(schemas.Artwork(id=item.id, name=item.name, is_active=item.is_active, layers=items, height=item.height, width=item.width))

#     # Sort by most recent submissions
#     # sorted_feed = sorted(artwork_list, key=lambda x: x.id, reverse=False)

#     return artwork_list
#     # return sorted_feed


# def get_artwork(db: Session, item_id: int) -> schemas.Artwork:
#     # Get layer for provided item_id
#     item = db.query(models.Item).filter(models.Item.id == item_id).first()
#     # Get all layers for base_layer_id
#     items_list = db.query(models.Item).filter(models.Item.base_layer_id == item.base_layer_id).filter(models.Item.id <= item.id).order_by(models.Item.id.desc()).all()
#     return schemas.Artwork(id=item.id, name=item.name, is_active=item.is_active, layers=items_list, height=item.height, width=item.width)


# async def get_artwork_history(db: Session, item_id: int) -> List[schemas.Artwork]:
#     item = db.query(models.Item).filter(models.Item.id == item_id).first()
#     items_list = db.query(models.Item).filter(models.Item.base_layer_id == item.base_layer_id).order_by(models.Item.id.desc()).all()
#     artwork_list = []
#     for item in items_list:
#         artwork_list.append(get_artwork(db, item.id))

#     return artwork_list


# def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
#     db_item = models.Item(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)

#     # If importing new art assign, given id to base_layer_id
#     if db_item.base_layer_id == None:
#         db_item.base_layer_id = db_item.id
#         db.commit()
#         db.refresh(db_item)

#     return db_item


# def delete_user_item(db: Session, item_id: int) -> models.Item:
#     db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
#     db.delete(db_item)
#     db.commit()
#     return db_item


# def delete_all_user_items(db: Session) -> List[models.Item]:
#     db_item = db.query(models.Item).filter(models.Item.owner_id != 1).all()
#     for item in db_item:
#         db.delete(item)
#     db.commit()
#     return db_item
