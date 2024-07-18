from typing import Optional

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from backend.session import create_session
from models.measurements import MeasurementModel
from schemas.measurements import Measurement

TAG = "Measurements"

router = APIRouter(prefix=f"/{TAG.lower()}")


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
    post = MeasurementModel(**payload.dict())
    session.add(post)
    session.commit()
    session.refresh(post)
