from sqlalchemy.orm import Session
from .database import engine
from sqlalchemy import event
from . import models
session = Session(engine, future=True)

INITIAL_DATA = {
    'users': [
        {
            "name": "The Thunder Shower",
            "owner_id": 1,
            "base_layer_id": 1
        },
        {
            "name": "Naked Ladies",
            "owner_id": 1,
            "base_layer_id": 2
        },
        {
            "name": "The Bedroom",
            "owner_id": 1,
            "base_layer_id": 3
        },
        {
            "name": "Mona Lisa",
            "owner_id": 1,
            "base_layer_id": 4
        },
        {
            "name": "The Scream",
            "owner_id": 1,
            "base_layer_id": 5
        },
        {
            "name": "Self Portrait",
            "owner_id": 1,
            "base_layer_id": 6
        }
    ]
}


def initialize_table(target, session, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        session.execute(target.insert(), INITIAL_DATA[tablename])


event.listen(models.Item.__table__, 'after_create', initialize_table)
event.listen(models.User.__table__, 'after_create', initialize_table)
