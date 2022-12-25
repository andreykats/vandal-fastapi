from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas
# import numpy as np
# from database import engine

# session = Session(engine, future=True)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_feed_items(db: Session):
    # Get all base_layer_ids and flatten to remove tuple
    base_ids = [id for id, in db.execute(select(models.Item.base_layer_id))]

    # Return unique
    unique_base_ids = set(base_ids)

    # Create a new feed array
    feed = []

    # For every base_id add the most recent layer created
    for id in unique_base_ids:
        result = db.query(models.Item).filter(models.Item.base_layer_id == id).order_by(models.Item.id.desc()).first()
        feed.append(result)

    return feed


def get_row_items(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.base_layer_id == item_id).order_by(models.Item.id.desc()).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # If importing new art assign, given id to base_layer_id
    if db_item.base_layer_id == None:
        db_item.base_layer_id = db_item.id
        db.commit()
        db.refresh(db_item)

    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()

    return {"status": "done"}

# def create_item_bulk(db: Session, items: list[schemas.ItemCreate]):
#     created = []
#     for item in items:
#         db_item = models.Item(**item.dict())
#         db.add(db_item)
#         db.commit()
#         db.refresh(db_item)
#         created.append(db_item)
#     return created
