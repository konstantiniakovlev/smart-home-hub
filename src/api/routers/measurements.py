import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Response
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.backend.session import create_session, create_async_session
from src.api.models.devices import DeviceModel
from src.api.models.measurements import MeasurementModel
from src.api.models.tags import TagModel
from src.api.schemas.measurements import Measurement


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
async def get_measurement_data(
        response: Response,
        device_id: int,
        sensor_tag: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        session: Session = Depends(create_session),
        async_session: AsyncSession = Depends(create_async_session)
):
    # todo: implement TTL Cache
    if not device_exists(device_id=device_id, session=session):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Device does not exist"

    query = select(MeasurementModel)\
        .where(MeasurementModel.device_id == device_id)

    if sensor_tag is not None:
        query = query.where(MeasurementModel.sensor_tag.contains(sensor_tag.upper()))

    if start_time is not None:
        query = query.where(MeasurementModel.time >= start_time)

    if end_time is not None:
        query = query.where(MeasurementModel.time <= end_time)

    result = await async_session.execute(query)
    return result.scalars().all()


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

    if not sensor_exists(sensor_tag=measurement.sensor_tag, session=session):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Sensor tag does not exist"

    session.add(measurement)
    session.commit()
    session.refresh(measurement)


def device_exists(device_id: int, session: Session):
    device_query = session.query(DeviceModel).filter(DeviceModel.device_id == device_id)
    if device_query.first() is None:
        return False
    return True


def sensor_exists(sensor_tag: str, session: Session):
    tag_query = session.query(TagModel).filter(TagModel.tag == sensor_tag)
    if tag_query.first() is None:
        return False
    return True
