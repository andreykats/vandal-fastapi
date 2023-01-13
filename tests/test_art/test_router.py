import json


def create_item(client):
    data = [
        {
            "name": "Mona Lisa",
            "owner_id": 1,
            "base_layer_id": 4
        }
    ]

    response = client.post(url='/art/', content=json.dumps(data))
    return response


def test_create_item(client):
    response = create_item(client)
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Mona Lisa"
    assert response.json()[0]["id"] == 1


def test_get_all_items(client):
    create_item(client)
    response = client.get("/art/")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Mona Lisa"
    assert response.json()[0]["id"] == 1


def test_get_item(client):
    create_item(client)
    response = client.get("/art/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mona Lisa"


def test_delete_item(client):
    create_item(client)
    response = client.delete("/art/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mona Lisa"
