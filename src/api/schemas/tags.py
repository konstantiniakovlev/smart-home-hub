from pydantic import BaseModel, Field
from typing import Union


class Tag(BaseModel):
    name: str = Field(...)
    tag: str = Field(primary_key=True)
    description: Union[str, None] = Field(default=None)

    class Config:
        orm_mode = True
