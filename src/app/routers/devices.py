from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas.devices import DeviceSchema, PostDevice
from backend.session import create_session
from models.devices import DeviceModel


TAG = "Devices"

router = APIRouter(prefix="/devices")


@router.get(
    path="/",
    summary="Get One or Every Device",
    description="Query one or every device registered in the house using device ID or MAC address.",
    tags=[TAG],
    response_model=list[DeviceSchema]
)
def get_devices(
        device_id: Optional[int] = None,
        mac_address: Optional[str] = None,
        session: Session = Depends(create_session)
):
    response = session.query(DeviceModel)
    if device_id is not None:
        response = response.filter(DeviceModel.device_id == device_id)
    if mac_address is not None:
        response = response.filter(DeviceModel.mac_address == mac_address)
    return response.all()


@router.post(
    path="/register",
    summary="Register Specific Device",
    description="Register a device using its MAC address.",
    tags=[TAG],
    status_code=status.HTTP_201_CREATED,
)
def register_device(payload: PostDevice, session: Session = Depends(create_session)):

    response = session.query(DeviceModel) \
        .filter(DeviceModel.mac_address == payload.mac_address)

    if response.first() is None:
        post = DeviceModel(**payload.dict())
        session.add(post)
        session.commit()
        session.refresh(post)

    else:
        response.update(payload.dict(), synchronize_session=False)
        session.commit()


@router.delete(
    path="/delete/{device_id}",
    summary="Delete Specific Device",
    description="Delete a device using device ID.",
    tags=[TAG],
    status_code=status.HTTP_200_OK
)
def delete_device(device_id: int, session: Session = Depends(create_session)):
    response = session.query(DeviceModel).filter(DeviceModel.device_id == device_id)

    if response.first() is not None:
        session.delete(response.first())
        session.commit()
