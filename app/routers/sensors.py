from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sensors import Sensor
from app.schemas import SensorCreate, SensorResponse

router = APIRouter(prefix="/sensors")


@router.post("/", status_code=201, response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    """Create a new sensor in the database.

    Args:
        sensor: The sensor data to create.
        db: Database session dependency.

    Returns:
        The newly created sensor with its assigned ID.
    """
    item = Sensor(**sensor.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)
    return item
