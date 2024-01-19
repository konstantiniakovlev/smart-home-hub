from typing import Union

from pydantic import BaseModel, Field


class DeviceSchema(BaseModel):
    mac_address: str
    ip_address: str
    device_type: str
    description: Union[str, None] = Field(default=None)

    class Config:
        orm_mode = True


class PostDevice(DeviceSchema):
    class Config:
        orm_mode = True
