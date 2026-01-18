from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.metrics import Metric
from app.schemas import MetricCreate, MetricQuery, MetricQueryResponse, MetricResponse

STAT_FUNCS = {
    "average": func.avg,
    "max": func.max,
    "min": func.min,
    "sum": func.sum,
}

router = APIRouter(prefix="/metrics")


@router.post("/", status_code=201, response_model=MetricResponse)
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    """Create a new metric record in the database.

    Args:
        metric: The metric data to create.
        db: Database session dependency.

    Returns:
        The newly created metric with its assigned ID.

    Raises:
        HTTPException: 409 if the referenced sensor_id doesn't exist.
    """
    try:
        record = Metric(**metric.model_dump())

        db.add(record)
        db.commit()
        db.refresh(record)

        return record
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Integrity error: Sensor id doesn't exist."
        )


@router.get(
    "/query",
    response_model=list[MetricQueryResponse],
    response_model_exclude_unset=True,
)
def get_metrics(query: Annotated[MetricQuery, Query()], db: Session = Depends(get_db)):
    """Query metrics with aggregation statistics.

    Retrieves metrics filtered by sensors, metric names, and date range,
    then applies the specified statistical aggregation (average, max, min, sum).

    Args:
        query: Query parameters including sensors, metrics, date range, and statistic type.
        db: Database session dependency.

    Returns:
        List of aggregated metric results grouped by sensor_id and metric_name.

    Raises:
        HTTPException: 404 if no data matches the query criteria.
    """
    statistic = query.statistic.lower()
    stat_func = STAT_FUNCS.get(statistic)

    query_stmnt = (
        select(
            Metric.sensor_id,
            Metric.metric_name,
            stat_func(Metric.metric_value).label(statistic),
        )
        .where(
            Metric.sensor_id.in_(query.sensors),
            Metric.metric_name.in_(query.metrics),
            Metric.created_at >= query.date_from,
            Metric.created_at <= query.date_to,
        )
        .group_by(Metric.sensor_id, Metric.metric_name)
    )

    result = db.execute(query_stmnt).all()

    if not result:
        raise HTTPException(
            status_code=404, detail="No data found for the given query."
        )

    return result
