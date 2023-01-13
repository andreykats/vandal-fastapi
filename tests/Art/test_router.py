from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import api
from app.dependencies import get_db
from app.database import Base

import json
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


api.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(api)


def create_item():
    data = [
        {
            "name": "Mona Lisa",
            "owner_id": 1,
            "base_layer_id": 4
        }
    ]

    response = client.post(url='/art/', content=json.dumps(data))
    return response


def test_create_item(test_db):
    response = create_item()
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Mona Lisa"
    assert response.json()[0]["id"] == 1


def test_get_all_items(test_db):
    create_item()
    response = client.get("/art/")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Mona Lisa"
    assert response.json()[0]["id"] == 1


def test_get_item(test_db):
    create_item()
    response = client.get("/art/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mona Lisa"


def test_delete_item(test_db):
    create_item()
    response = client.delete("/art/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mona Lisa"
