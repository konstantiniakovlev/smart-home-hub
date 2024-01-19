from typing import Union

from pydantic import BaseModel, Field


class ProgramSchema(BaseModel):
    device_id: int
    port: int
    description: Union[str, None] = Field(default=None)

    class Config:
        orm_mode = True


class PostProgram(ProgramSchema):
    class Config:
        orm_mode = True
