from fastapi import APIRouter, Depends, Query
from app.database import get_db
from app.models.sensors import Sensor
from app.schemas import SensorCreate, SensorResponse


router = APIRouter(prefix="/sensors")


@router.post("/", status_code=201, response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db=Depends(get_db)):
    item = Sensor(**sensor.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)
    return item
