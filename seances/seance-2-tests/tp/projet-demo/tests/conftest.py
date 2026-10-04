import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items, reservations

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_storage():
    items.FAKE_DB.clear()
    reservations.FAKE_DB.clear()
    
@pytest.fixture
def item(client: TestClient) -> dict:
    response = client.post(
        "/items",
        json={
            "titre": "Caméra Sony",
            "description": "Caméra pour tournage",
            "tarif_jour": 25.0,
            "disponible": True,
        },
    )

    assert response.status_code == 201

    return response.json()