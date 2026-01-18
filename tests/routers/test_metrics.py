from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


def test_create_metric(test_db):
    response = client.post(
        "/metrics/",
        json={"sensor_id": 1, "metric_name": "temperature", "metric_value": 23},
    )

    assert response.status_code == 201
    assert response.json()["sensor_id"] == 1
    assert response.json()["metric_name"] == "temperature"
    assert response.json()["metric_value"] == 23


def test_create_metric_invalid_sensor(test_db):
    response = client.post(
        "/metrics/",
        json={"sensor_id": 999, "metric_name": "temperature", "metric_value": 23},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Integrity error: Sensor id doesn't exist."


@pytest.mark.parametrize(
    "query_params, expected_response",
    [
        (
            "sensors=1&metrics=temperature&statistic=average&date_from=2025-01-01&date_to=2025-01-31",
            [{"sensor_id": 1, "metric_name": "temperature", "average": 23.5}],
        ),
        (
            "sensors=1,2&metrics=temperature,humidity&statistic=min&date_from=2025-01-01&date_to=2025-01-15",
            [
                {"sensor_id": 1, "metric_name": "humidity", "min": 55.0},
                {"sensor_id": 1, "metric_name": "temperature", "min": 32.0},
                {"sensor_id": 2, "metric_name": "humidity", "min": 45.0},
            ],
        ),
        (
            "sensors=2&metrics=humidity&statistic=max",
            [
                {"sensor_id": 2, "metric_name": "humidity", "max": 35.0},
            ],
        ),
    ],
)
def test_get_metrics(query_params, expected_response, test_db):
    response = client.get("metrics/query?" + query_params)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_metrics_invalid_requests(test_db):
    response = client.get("metrics/query?sensors=1&metrics=temperature&statistic=fake_stat")
    assert "Statistic must be one of " in response.text
    
    response = client.get("metrics/query?sensors=1&metrics=temperature&statistic=average&date_from=2025-01-01")
    assert response.text == "Validation errors:\nField: ('query',), Error: Value error, Both date_from and date_to must be provided together."

    response = client.get("metrics/query?sensors=1&metrics=temperature&statistic=average&date_from=2025-01-01&date_to=12-31-2025")
    assert response.text == "Validation errors:\nField: ('query', 'date_to'), Error: Value error, Date must be in ISO format YYYY-MM-DD."