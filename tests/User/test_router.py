from fastapi.testclient import TestClient
from app.main import api

client = TestClient(api)


def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200