from fastapi.testclient import TestClient


def test_create_item(client: TestClient) -> None:
    payload = {
        "titre": "Caméra Sony",
        "description": "Caméra pour tournage",
        "tarif_jour": 25.0,
        "disponible": True,
    }

    response = client.post("/items", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["titre"] == "Caméra Sony"
    assert data["description"] == "Caméra pour tournage"
    assert data["tarif_jour"] == 25.0
    assert data["disponible"] is True
    
def test_list_items(client: TestClient) -> None:
    client.post(
        "/items",
        json={
            "titre": "Caméra Sony",
            "description": "Caméra pour tournage",
            "tarif_jour": 25.0,
            "disponible": True,
        },
    )

    client.post(
        "/items",
        json={
            "titre": "Trépied",
            "description": "Trépied vidéo",
            "tarif_jour": 10.0,
            "disponible": False,
        },
    )

    response = client.get("/items")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["titre"] == "Caméra Sony"
    assert data[1]["titre"] == "Trépied"
    
def test_list_items_filters(client: TestClient) -> None:
    client.post(
        "/items",
        json={
            "titre": "Caméra Sony",
            "description": "Caméra professionnelle",
            "tarif_jour": 25.0,
            "disponible": True,
        },
    )

    client.post(
        "/items",
        json={
            "titre": "Trépied vidéo",
            "description": "Support pour caméra",
            "tarif_jour": 10.0,
            "disponible": False,
        },
    )

    client.post(
        "/items",
        json={
            "titre": "Microphone",
            "description": "Micro professionnel",
            "tarif_jour": 15.0,
            "disponible": True,
        },
    )

    response = client.get("/items?q=caméra")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get("/items?disponible=true")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get("/items?disponible=false")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["titre"] == "Trépied vidéo"

    response = client.get("/items?skip=1&limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["titre"] == "Trépied vidéo"
    
def test_get_item(client: TestClient, item: dict) -> None:
    item_id = item["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["titre"] == "Caméra Sony"
    assert data["tarif_jour"] == 25.0


def test_get_item_not_found(client: TestClient) -> None:
    response = client.get("/items/999")

    assert response.status_code == 404
    
def test_update_item(client: TestClient, item: dict) -> None:
    item_id = item["id"]

    response = client.put(
        f"/items/{item_id}",
        json={
            "titre": "Caméra Canon",
            "description": "Nouvelle description",
            "tarif_jour": 30.0,
            "disponible": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["titre"] == "Caméra Canon"
    assert data["description"] == "Nouvelle description"
    assert data["tarif_jour"] == 30.0
    assert data["disponible"] is False
    
def test_patch_item(client: TestClient, item: dict) -> None:
    item_id = item["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={
            "tarif_jour": 30.0,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["titre"] == "Caméra Sony"
    assert data["description"] == "Caméra pour tournage"
    assert data["tarif_jour"] == 30.0
    assert data["disponible"] is True
    
def test_delete_item(client: TestClient, item: dict) -> None:
    item_id = item["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 204

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 404
    
    
def test_update_item_not_found(client: TestClient) -> None:
    response = client.put(
        "/items/999",
        json={
            "titre": "Caméra Canon",
            "description": "Nouvelle description",
            "tarif_jour": 30.0,
            "disponible": False,
        },
    )

    assert response.status_code == 404


def test_patch_item_not_found(client: TestClient) -> None:
    response = client.patch(
        "/items/999",
        json={
            "tarif_jour": 30.0,
        },
    )

    assert response.status_code == 404


def test_delete_item_not_found(client: TestClient) -> None:
    response = client.delete("/items/999")

    assert response.status_code == 404