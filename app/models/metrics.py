from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base
from app.models.sensors import Sensor


class Metric(Base):
    __tablename__ = "metrics"

    metric_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sensor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Sensor.sensor_id), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    metric_name: Mapped[str] = mapped_column(String, nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
