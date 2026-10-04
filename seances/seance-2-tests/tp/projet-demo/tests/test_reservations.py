from fastapi.testclient import TestClient


def test_create_reservation(client: TestClient, item: dict) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-12",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["item_id"] == item["id"]
    assert data["date_debut"] == "2026-10-10"
    assert data["date_fin"] == "2026-10-12"
    assert data["statut"] == "active"
    
    
def test_create_reservation_invalid_dates(
    client: TestClient,
    item: dict,
) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-12",
            "date_fin": "2026-10-10",
        },
    )

    assert response.status_code == 422
    
def test_list_reservations(client: TestClient, item: dict) -> None:
    client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-12",
        },
    )

    client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-15",
            "date_fin": "2026-10-17",
        },
    )

    response = client.get("/reservations")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2
    assert data[0]["statut"] == "active"
    assert data[1]["statut"] == "active"
    
def test_list_reservations_by_item(
    client: TestClient,
    item: dict,
) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-12",
        },
    )
    assert response.status_code == 201

    response = client.get(
        f"/reservations?item_id={item['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["item_id"] == item["id"]
    
def test_get_reservation(
    client: TestClient,
    item: dict,
) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-12",
        },
    )

    assert response.status_code == 201

    reservation = response.json()

    reservation_id = reservation["id"]

    response = client.get(f"/reservations/{reservation_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reservation_id
    assert data["item_id"] == item["id"]
    assert data["statut"] == "active"


def test_get_reservation_not_found(client: TestClient) -> None:
    response = client.get("/reservations/999")

    assert response.status_code == 404
    
def test_cancel_reservation(
    client: TestClient,
    item: dict,
) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-12",
        },
    )

    assert response.status_code == 201

    reservation_id = response.json()["id"]

    response = client.post(
        f"/reservations/{reservation_id}/annuler"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reservation_id
    assert data["statut"] == "annulee"


def test_cancel_reservation_twice(
    client: TestClient,
    item: dict,
) -> None:
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-12",
        },
    )

    assert response.status_code == 201

    reservation_id = response.json()["id"]

    response = client.post(
        f"/reservations/{reservation_id}/annuler"
    )
    assert response.status_code == 200

    response = client.post(
        f"/reservations/{reservation_id}/annuler"
    )

    assert response.status_code == 409
    
def test_cancel_reservation_not_found(client: TestClient) -> None:
    response = client.post(
        "/reservations/999/annuler"
    )

    assert response.status_code == 404