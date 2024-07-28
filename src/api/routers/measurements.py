import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Response
from starlette import status
from sqlalchemy.orm import Session

from backend.session import create_session
from models.devices import DeviceModel
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
    response_model=list[Measurement] | str
)
def get_measurement_data(
        response: Response,
        device_id: int,
        sensor_tag: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        session: Session = Depends(create_session)
):
    if not device_exists(device_id=device_id, session=session):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Device does not exist"

    query = session.query(MeasurementModel)\
        .filter(MeasurementModel.device_id == device_id)

    if sensor_tag is not None:
        query = query.filter(MeasurementModel.sensor_tag == sensor_tag)

    if start_time is not None:
        query = query.filter(MeasurementModel.time >= start_time)

    if end_time is not None:
        query = query.filter(MeasurementModel.time <= end_time)

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
        response: Response,
        session: Session = Depends(create_session)
):
    measurement = MeasurementModel(**payload.dict())

    if not device_exists(device_id=measurement.device_id, session=session):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Device does not exist"

    session.add(measurement)
    session.commit()
    session.refresh(measurement)


def device_exists(device_id: int, session: Session):
    device_query = session.query(DeviceModel).filter(DeviceModel.device_id == device_id)
    if device_query.first() is None:
        return False
    return True

