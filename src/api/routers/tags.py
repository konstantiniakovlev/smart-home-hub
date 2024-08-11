from typing import Optional

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from backend.session import create_session
from models.tags import TagModel
from schemas.tags import Tag


TAG = "Tags"

router = APIRouter(prefix=f"/{TAG.lower()}")


@router.get(
    path="/",
    summary="Get Sensor Tag Information",
    description="",
    tags=[TAG],
    status_code=status.HTTP_200_OK,
    response_model=list[Tag]
)
def get_tags(
        name_filter: Optional[str] = None,
        sensor_tag: Optional[str] = None,
        session: Session = Depends(create_session)
):
    query = session.query(TagModel)
    if name_filter is not None:
        query = query.filter(TagModel.name.contains(name_filter.title()))
    if sensor_tag is not None:
        query = query.filter(TagModel.tag == sensor_tag.upper())
    return query.all()
