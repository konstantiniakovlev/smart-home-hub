import datetime

from pydantic import BaseModel, Field
from typing import Union


class Measurement(BaseModel):
    time: Union[datetime.datetime, None] = Field(default=None)
    device_id: int = Field(...)
    sensor_tag: str = Field(...)
    value: float = Field(...)

    class Config:
        orm_mode = True
