from typing import Optional

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from backend.session import create_session
from models.measurements import MeasurementModel
from schemas.measurements import Measurement

TAG = "Measurements"

router = APIRouter(prefix=f"/{TAG.lower()}")


@router.get(
    path="/{device_id}",
    summary="Get Measurement Data",
    description="",
    tags=[TAG],
    status_code=status.HTTP_200_OK,
    response_model=list[Measurement]
)
def get_measurement_data(
        device_id: int,
        sensor_tag: Optional[str] = None,
        session: Session = Depends(create_session)
):
    query = session.query(MeasurementModel)\
        .filter(MeasurementModel.device_id == device_id)
    if sensor_tag is not None:
        query = query.filter(MeasurementModel.sensor_tag == sensor_tag)
    return query.all()


@router.post(
    path="/",
    summary="Store Measurement",
    description="",
    tags=[TAG],
    status_code=status.HTTP_201_CREATED
)
def store_measurement(
        payload: Measurement,
        session: Session = Depends(create_session)
):
    measurement = MeasurementModel(**payload.dict())
    session.add(measurement)
    session.commit()
    session.refresh(measurement)
