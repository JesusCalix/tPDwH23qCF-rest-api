from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db
from app.models.metrics import Metric
from app.schemas import MetricCreate, MetricResponse, MetricQueryResponse, MetricQuery
from sqlalchemy.exc import IntegrityError
from typing import Annotated

router = APIRouter(prefix="/metrics")


@router.post("/", status_code=201, response_model=MetricResponse)
def create_metric(metric: MetricCreate, db=Depends(get_db)):
    try:
        record = Metric(**metric.model_dump())

        db.add(record)
        db.commit()
        db.refresh(record)

        return record
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Integrity error: Sensor id doesn't exist."
        )


@router.get(
    "/query",
    response_model=list[MetricQueryResponse],
    response_model_exclude_unset=True,
)
def get_metrics(query: Annotated[MetricQuery, Query()], db=Depends(get_db)):
    print("Query Params:", query)

    query_db = db.query(Metric).filter(
        Metric.sensor_id.in_(query.sensors),
        Metric.metric_name.in_(query.metrics),
        Metric.created_at >= query.date_from,
        Metric.created_at <= query.date_to,
    )

    statistic = query.statistic.lower()

    if statistic == "average":
        query_db = query_db.group_by(
            Metric.sensor_id, Metric.metric_name
        ).with_entities(
            Metric.sensor_id,
            Metric.metric_name,
            func.avg(Metric.metric_value).label("average"),
        )
    elif statistic == "max":
        query_db = query_db.group_by(
            Metric.sensor_id, Metric.metric_name
        ).with_entities(
            Metric.sensor_id,
            Metric.metric_name,
            func.max(Metric.metric_value).label("max"),
        )
    elif statistic == "min":
        query_db = query_db.group_by(
            Metric.sensor_id, Metric.metric_name
        ).with_entities(
            Metric.sensor_id,
            Metric.metric_name,
            func.min(Metric.metric_value).label("min"),
        )
    elif statistic == "sum":
        query_db = query_db.group_by(
            Metric.sensor_id, Metric.metric_name
        ).with_entities(
            Metric.sensor_id,
            Metric.metric_name,
            func.sum(Metric.metric_value).label("sum"),
        )

    result = query_db.all()

    if not result:
        raise HTTPException(
            status_code=404, detail="No data found for the given query."
        )

    return result

