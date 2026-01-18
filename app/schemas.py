from typing import Optional
from pydantic import BaseModel, model_validator, field_validator, ConfigDict
from datetime import datetime, time


class SensorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Sensor name must not be empty.")
        return v.strip()


class SensorResponse(BaseModel):
    sensor_id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class MetricCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sensor_id: int
    metric_name: str
    metric_value: float

    @field_validator("metric_name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Metric name must not be empty.")
        return v.strip()


class MetricResponse(BaseModel):
    sensor_id: int
    metric_name: str
    metric_value: float

    class Config:
        from_attributes = True


class MetricQuery(BaseModel):
    sensors: str
    metrics: str
    statistic: str
    date_from: Optional[str] = None
    date_to: Optional[str] = None

    @field_validator("sensors")
    @classmethod
    def split_sensors(csl, values):
        return [int(v) for v in values.split(",")]

    @field_validator("metrics")
    @classmethod
    def split_metrics(cls, values):
        return [v.strip().lower() for v in values.split(",")]

    @field_validator("statistic")
    @classmethod
    def validate_statistic(cls, v):
        valid_stats = {"average", "min", "max", "sum"}
        if v.lower() not in valid_stats:
            raise ValueError(f"Statistic must be one of {valid_stats}.")

        return v.lower()

    @model_validator(mode="before")
    @classmethod
    def ensure_both_dates_or_none(cls, values):
        date_from = values.get("date_from")
        date_to = values.get("date_to")
        if date_from is None and date_to is None:
            today = datetime.today().date()
            values["date_from"] = datetime.combine(today, time.min).isoformat()
            values["date_to"] = datetime.combine(today, time(23, 59)).isoformat()
        elif (date_from is None) != (date_to is None):
            raise ValueError("Both date_from and date_to must be provided together.")

        return values

    @field_validator("date_from", "date_to")
    @classmethod
    def process_dates(cls, date_str):
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            raise ValueError("Date must be in ISO format YYYY-MM-DD.")


class MetricQueryResponse(BaseModel):
    sensor_id: int
    metric_name: str
    average: Optional[float] | None = None
    min: Optional[float] | None = None
    max: Optional[float] | None = None
    sum: Optional[float] | None = None

    class Config:
        from_attributes = True
