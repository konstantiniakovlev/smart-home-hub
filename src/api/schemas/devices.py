import datetime

from pydantic import BaseModel, Field
from typing import Union


class Device(BaseModel):
    device_id: int = Field(primary_key=True)
    mac_address: str = Field(...)
    ip_address: str = Field(...)
    device_type: str = Field(...)
    description: Union[str, None] = Field(default=None)
    registered_at: datetime.datetime = Field(...)
    updated_at: datetime.datetime = Field(...)

    class Config:
        orm_mode = True


class RegisterDevice(BaseModel):
    mac_address: str = Field(...)
    ip_address: str = Field(...)
    device_type: str = Field(...)
    description: Union[str, None] = Field(default=None)

    class Config:
        orm_mode = True

