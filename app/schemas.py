from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator, Field


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
    model_config = ConfigDict(from_attributes=True)

    sensor_id: int
    name: str
    created_at: datetime


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
    model_config = ConfigDict(from_attributes=True)

    sensor_id: int
    metric_name: str
    metric_value: float


class MetricQuery(BaseModel):
    sensors: str = Field(
        description="Comma-separated list of sensor IDs (e.g., '1,2,3')"
    )
    metrics: str = Field(
        description="Comma-separated list of metric names (e.g., 'temperature,humidity')"
    )
    statistic: str = Field(
        description="Statistical aggregation to apply: average, min, max, sum"
    )
    date_from: Optional[str] = Field(
        default=None, description="Start date in ISO format (YYYY-MM-DD)"
    )
    date_to: Optional[str] = Field(
        default=None, description="End date in ISO format (YYYY-MM-DD)"
    )

    @field_validator("sensors")
    @classmethod
    def split_sensors(csl, values):
        try:
            return [int(v) for v in values.split(",")]
        except ValueError:
            raise ValueError("Sensors must be a comma-separated list of integers.")

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
    model_config = ConfigDict(from_attributes=True)
    sensor_id: int
    metric_name: str
    average: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    sum: Optional[float] = None
