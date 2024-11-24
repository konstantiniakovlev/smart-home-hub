from fastapi import APIRouter
from starlette import status

from schemas.health import HealthCheck


TAG = "Health checks"

router = APIRouter(prefix="/health")


@router.get(
    path="/",
    summary="Perform a health check",
    description="",
    tags=[TAG],
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")
