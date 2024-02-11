from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.session import create_session
from models.programs import ProgramModel
from schemas.programs import ProgramSchema, PostProgram


TAG = "Programs"

router = APIRouter(prefix="/programs")


@router.get(
    path="/",
    summary="Get Program Information",
    description="Query one or multiple programs "
                "registered in the house using device ID, "
                "program ID, or port number.",
    tags=[TAG],
    response_model=list[ProgramSchema]
)
def get_programs(
        device_id: Optional[int] = None,
        program_id: Optional[int] = None,
        port: Optional[int] = None,
        session: Session = Depends(create_session)
):
    response = session.query(ProgramModel)
    if device_id is not None:
        response = response.filter(ProgramModel.device_id == device_id)
    if program_id is not None:
        response = response.filter(ProgramModel.program_id == program_id)
    if port is not None:
        response = response.filter(ProgramModel.port == port)
    return response.all()


@router.post(
    path="/register",
    summary="Register Program",
    description="Register a program on a device using "
                "device ID and configured port. "
                "If port is in use, the entry with same "
                "port number is updated.",
    tags=[TAG],
    status_code=status.HTTP_201_CREATED
)
def register_program(payload: PostProgram, session: Session = Depends(create_session)):

    response = session.query(ProgramModel) \
        .filter(ProgramModel.device_id == payload.device_id)

    if payload.port is not None:
        response = response.filter(ProgramModel.port == payload.port)
    else:
        response = response \
            .filter(ProgramModel.port.is_(None)) \
            .filter(ProgramModel.program_name == payload.program_name)

    if response.first() is None:
        post = ProgramModel(**payload.dict())
        session.add(post)
        session.commit()
        session.refresh(post)
    else:
        response.update(payload.dict(), synchronize_session=False)
        session.commit()


@router.delete(
    path="/delete",
    summary="Delete Program",
    description="Delete one or multiple program entries "
                "using device ID, program ID, port number, "
                "and program name.",
    tags=[TAG],
    status_code=status.HTTP_200_OK
)
def delete_program(
        device_id: int,
        program_id: Optional[int] = None,
        port: Optional[int] = None,
        program_name: Optional[str] = None,
        session: Session = Depends(create_session)
):
    response = session.query(ProgramModel) \
        .filter(ProgramModel.device_id == device_id)

    if program_id is not None:
        response = response \
            .filter(ProgramModel.program_id == program_id)

    if port is not None:
        response = response \
            .filter(ProgramModel.port == port)

    if program_name is not None:
        response = response \
            .filter(ProgramModel.program_name == program_name)

    if response.first() is not None:
        response.delete()
        session.commit()
