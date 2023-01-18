from .db_sql import SessionLocal
from .db_dynamo import Service


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_ddb():
    return Service
