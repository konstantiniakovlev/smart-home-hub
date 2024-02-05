from typing import Union

import datetime
from pydantic import BaseModel, Field


class DeviceSchema(BaseModel):
    device_id: int = Field(primary_key=True)
    mac_address: str
    ip_address: str
    device_type: str
    description: Union[str, None] = Field(default=None)
    registered_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class PostDevice(BaseModel):
    mac_address: str
    ip_address: str
    device_type: str
    description: Union[str, None] = Field(default=None)

    class Config:
        orm_mode = True
