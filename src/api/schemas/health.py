from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str = "OK"

    class Config:
        orm_mode = True
