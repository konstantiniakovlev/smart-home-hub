import datetime

from pydantic import BaseModel, Field


class Measurement(BaseModel):
    time: datetime.datetime = Field(default=None)
    device_id: int = Field(...)
    sensor_tag: str = Field(...)
    value: float = Field(...)

    class Config:
        orm_mode = True
