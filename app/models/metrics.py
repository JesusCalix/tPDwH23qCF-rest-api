from app.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from app.models.sensors import Sensor


class Metric(Base):
    __tablename__ = "metrics"

    metric_id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey(Sensor.sensor_id), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    metric_name = Column(Text, nullable=False)
    metric_value = Column(Float, nullable=False)
