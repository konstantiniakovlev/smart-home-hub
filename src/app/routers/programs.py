from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas.programs import ProgramSchema, PostProgram
from backend.session import create_session
from models.programs import ProgramModel
from models.devices import DeviceModel


TAG = "Programs"

router = APIRouter(prefix="/programs")


@router.get(
    path="/",
    summary="Get Parameters of Every Program",
    description="Receive parameters of all programs currently set up in house.",
    tags=[TAG],
    response_model=list[ProgramSchema]
)
def get_programs(session: Session = Depends(create_session)):
    response = session.query(ProgramModel).all()
    return response


@router.get(
    path="/{device_id}",
    summary="Get Every Program on Specific Device",
    description="Receive parameters of all programs set on selected device.",
    tags=[TAG],
    response_model=list[ProgramSchema]
)
def get_device_programs(device_id: int, session: Session = Depends(create_session)):
    response = session.query(ProgramModel).filter(ProgramModel.device_id == device_id)
    return response


@router.post(
    path="/register",
    summary="Register Program on Specific Device",
    description="Register new program on a device using device ID.",
    tags=[TAG],
    status_code=status.HTTP_201_CREATED,
)
def register(payload: PostProgram, session: Session = Depends(create_session)):

    response = session.query(DeviceModel).filter(DeviceModel.device_id == payload.device_id)
    if response.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with device_id={payload.device_id} not registered."
        )

    response = session.query(ProgramModel)\
        .filter(ProgramModel.device_id.split() == payload.device_id)\
        .filter(ProgramModel.port == payload.port)

    if response.first() is None:
        post = ProgramModel(**payload.dict())
        session.add(post)
        session.commit()
        session.refresh(post)

    else:
        response.update(payload.dict(), synchronize_session=False)
        session.commit()
