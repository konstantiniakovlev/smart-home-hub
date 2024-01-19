from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from schemas.devices import DeviceSchema, PostDevice
from backend.session import create_session
from models.devices import DeviceModel


TAG = "Devices"

router = APIRouter(prefix="/devices")


@router.get(
    path="/",
    summary="Get Parameters of Every Device",
    description="Receive configuration parameters for all devices currently set up in house.",
    tags=[TAG],
    response_model=list[DeviceSchema]
)
def get_devices(session: Session = Depends(create_session)):
    response = session.query(DeviceModel).all()
    return response


@router.get(
    path="/{device_id}",
    summary="Get Parameters of Specific Device",
    description="Receive parameters of selected device.",
    tags=[TAG],
    response_model=list[DeviceSchema]
)
def get_device(device_id: int, session: Session = Depends(create_session)):
    response = session.query(DeviceModel).filter(DeviceModel.device_id == device_id)
    return response


@router.post(
    path="/register",
    summary="Register Program on Specific Device",
    description="Register new program on a device using device ID.",
    tags=[TAG],
    status_code=status.HTTP_201_CREATED,
)
def register(payload: PostDevice, session: Session = Depends(create_session)):

    response = session.query(DeviceModel) \
        .filter(DeviceModel.mac_address == payload.mac_address) \
        .filter(DeviceModel.dict().get("ip_address", "").split("/")[0] == payload.ip_address)

    if response.first() is None:
        post = DeviceModel(**payload.dict())
        session.add(post)
        session.commit()
        session.refresh(post)

    else:
        response.update(payload.dict(), synchronize_session=False)
        session.commit()
