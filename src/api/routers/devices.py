from typing import Optional

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from backend.session import create_session
from models.devices import DeviceModel
from schemas.devices import Device, RegisterDevice


TAG = "Devices"

router = APIRouter(prefix=f"/{TAG.lower()}")


@router.get(
    path="/",
    summary="Get Device Information",
    description="",
    tags=[TAG],
    status_code=status.HTTP_200_OK,
    response_model=list[Device]
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
    summary="Add Device to Registry",
    description="",
    tags=[TAG],
    status_code=status.HTTP_201_CREATED,
    response_model=list[Device]
)
def register_device(payload: RegisterDevice, session: Session = Depends(create_session)):

    response = session.query(DeviceModel) \
        .filter(DeviceModel.mac_address == payload.mac_address)

    if response.first() is None:
        device_obj = DeviceModel(**payload.dict())
        session.add(device_obj)
        session.commit()
        session.refresh(device_obj)

        return [device_obj]

    else:
        response.update(payload.dict(), synchronize_session=False)
        session.commit()

    return response.all()


@router.delete(
    path="/delete/{device_id}",
    summary="Delete Device from Registry",
    description="",
    tags=[TAG],
    status_code=status.HTTP_202_ACCEPTED
)
def delete_device(device_id: int, session: Session = Depends(create_session)):
    response = session.query(DeviceModel).filter(DeviceModel.device_id == device_id)

    device_obj = response.first()
    if device_obj is not None:
        session.delete(device_obj)
        session.commit()


