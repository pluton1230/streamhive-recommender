from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """La API debe responder 200 en /health."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "recommender"


def test_recommendations_basic():
    """El endpoint de recomendaciones debe devolver una lista no vacía."""
    response = client.get("/recommendations?user_id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0


def test_register_watch_event():
    """
    El endpoint /events/watch debe aceptar un evento
    y devolver un id (se almacena en la base de datos SQLite).
    """
    payload = {
        "user_id": 1,
        "video_id": 101,
        "seconds_watched": 45,
    }

    response = client.post("/events/watch", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "id" in data
    assert isinstance(data["id"], int)
