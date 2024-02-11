from pydantic import BaseModel
from typing import Dict, List, Union


class ConfigParams(BaseModel):
    name: str
    value: Union[float, int, str]


class PostInteraction(BaseModel):
    device_id: int
    port: int
    config_params: List[ConfigParams] = [
        {
            "name": "endpoint",
            "value": "activate"
        },
        {
            "name": "duration",
            "value": 5
        }
    ]

    class Config:
        orm_mode = True


class PostResponseSchema(BaseModel):
    device_id: int
    device_type: Union[str, None]
    ip_address: Union[str, None]
    port: int
    url: str
    request_body: Dict
    response: Dict
