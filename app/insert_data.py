from app.database import SessionLocal
from app.models.sensors import Sensor
from app.models.metrics import Metric
from datetime import datetime, timedelta
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError


def insert_sample_data():
    """
    Insert sample data into the database.
    """
    db = SessionLocal()

    try:
        now = datetime.today()

        db.execute(
            insert(Sensor),
            [
                {"name": "Sensor A", "created_at": datetime(2022, 1, 17, 15, 0, 0)},
                {"name": "Sensor B", "created_at": datetime(2024, 11, 30, 11, 0, 0)},
                {"name": "Sensor C", "created_at": now},
            ],
        )

        db.execute(
            insert(Metric),
            [
                {
                    "sensor_id": 1,
                    "created_at": now - timedelta(days=3),
                    "metric_name": "temperature",
                    "metric_value": 32.0,
                },
                {
                    "sensor_id": 1,
                    "created_at": now - timedelta(days=3),
                    "metric_name": "humidity",
                    "metric_value": 15.0,
                },
                {
                    "sensor_id": 1,
                    "created_at": now - timedelta(days=3),
                    "metric_name": "precipitation",
                    "metric_value": 35.0,
                },
                {
                    "sensor_id": 1,
                    "created_at": now - timedelta(days=2),
                    "metric_name": "temperature",
                    "metric_value": 15.0,
                },
                {
                    "sensor_id": 2,
                    "created_at": now - timedelta(days=60),
                    "metric_name": "wind speed",
                    "metric_value": 35.0,
                },
                {
                    "sensor_id": 2,
                    "created_at": now - timedelta(days=30),
                    "metric_name": "wind speed",
                    "metric_value": 12.0,
                },
                {
                    "sensor_id": 2,
                    "created_at": now - timedelta(days=30),
                    "metric_name": "temperature",
                    "metric_value": 25.0,
                },
                {
                    "sensor_id": 3,
                    "created_at": now - timedelta(days=30),
                    "metric_name": "temperature",
                    "metric_value": 22.0,
                },
                {
                    "sensor_id": 3,
                    "created_at": now - timedelta(days=15),
                    "metric_name": "temperature",
                    "metric_value": 15.0,
                },
            ],
        )
        db.commit()

    except IntegrityError:
        db.rollback()
    finally:
        db.close()
