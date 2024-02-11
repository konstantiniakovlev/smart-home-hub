from typing import Union

import datetime
from pydantic import BaseModel, Field


class ProgramSchema(BaseModel):
    program_id: int = Field(primary_key=True)
    device_id: int
    port: Union[int, None] = Field(default=None)
    program_name: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)
    registered_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class PostProgram(BaseModel):
    device_id: int
    port: Union[int, None] = Field(default=None)
    program_name: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)

    class Config:
        orm_mode = True
