from app.database import Base
from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.sql import func


class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
