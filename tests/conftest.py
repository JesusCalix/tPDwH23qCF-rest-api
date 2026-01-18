import os
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models.sensors import Sensor
from app.models.metrics import Metric
from sqlalchemy import insert
from datetime import datetime

# Create test database engine
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)


@event.listens_for(test_engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()

        test_sensor_data(db)
        test_metric_data(db)
        db.commit()
        db.close()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()

    # Delete test database file
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_sensor_data(db):
    db.execute(
        insert(Sensor),
        [
            {"name": "Sensor A", "created_at": datetime(2025, 1, 10, 15, 0, 0)},
            {"name": "Sensor B", "created_at": datetime(2025, 1, 18, 15, 0, 0)},
        ],
    )


def test_metric_data(db):
    db.execute(
        insert(Metric),
        [
            {
                "sensor_id": 1,
                "created_at": datetime(2025, 1, 10, 0, 0, 0),
                "metric_name": "temperature",
                "metric_value": 32,
            },
            {
                "sensor_id": 1,
                "created_at": datetime(2025, 1, 10, 0, 0, 0),
                "metric_name": "humidity",
                "metric_value": 55.0,
            },
            {
                "sensor_id": 1,
                "created_at": datetime(2025, 1, 18, 0, 0, 0),
                "metric_name": "temperature",
                "metric_value": 15,
            },
            {
                "sensor_id": 2,
                "created_at": datetime(2025, 1, 15, 0, 0, 0),
                "metric_name": "humidity",
                "metric_value": 45.0,
            },
            {
                "sensor_id": 2,
                "created_at": datetime(2025, 1, 18, 0, 0, 0),
                "metric_name": "humidity",
                "metric_value": 21.0,
            },
            {
                "sensor_id": 2,
                "created_at": datetime.today(),
                "metric_name": "humidity",
                "metric_value": 21.0,
            },
            {
                "sensor_id": 2,
                "created_at": datetime.today(),
                "metric_name": "humidity",
                "metric_value": 35.0,
            },
        ],
    )
