import json


def create_user(client):
    data = {
        "email": "andrey@greg.com",
        "password": "testing123"
    }

    response = client.post(url='/users/', content=json.dumps(data))
    return response


def test_create_user(client):
    response = create_user(client)
    assert response.status_code == 200
    assert response.json()["email"] == "andrey@greg.com"
    assert response.json()["id"] == 1


def test_get_all_users(client):
    create_user(client)
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()[0]["email"] == "andrey@greg.com"
    assert response.json()[0]["id"] == 1


def test_get_user(client):
    create_user(client)
    response = client.get("/users/1")
    assert response.json()["email"] == "andrey@greg.com"
    assert response.json()["id"] == 1
