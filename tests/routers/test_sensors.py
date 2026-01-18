from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_sensor(test_db):
    response = client.post("/sensors/", json={"name": "Test Sensor"})

    assert response.status_code == 201
    assert response.json()["sensor_id"] == 3
    assert response.json()["name"] == "Test Sensor"


def test_create_sensor_empty_name(test_db):
    response = client.post("/sensors/", json={"name": ""})

    assert response.status_code == 422
