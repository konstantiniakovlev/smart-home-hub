from typing import List

from fastapi import APIRouter, Depends
import requests
from sqlalchemy.orm import Session
from starlette import status

from backend.session import create_session
from models.devices import DeviceModel
from schemas.interactions import PostInteraction, PostResponseSchema


TAG = "Interactions"

router = APIRouter(prefix="/interactions")


@router.post(
    path="/",
    summary="Interact with Devices",
    description="Send one or multiple "
                "interaction requests to "
                "various devices using their "
                "device IDs and port numbers.",
    tags=[TAG],
    status_code=status.HTTP_207_MULTI_STATUS,
    response_model=List[PostResponseSchema]
)
def send_interaction_request(
        payload: List[PostInteraction],
        session: Session = Depends(create_session)
):

    responses = []
    for pl in payload:
        pl = pl.dict()
        device_id = pl.get("device_id")
        port = pl.get("port")
        data = {
            cp.get("name"): cp.get("value")
            for cp in pl.get("config_params", [])
        }
        endpoint = data.get('endpoint', None)

        query_response = (
            session.query(DeviceModel)
            .filter(DeviceModel.device_id == device_id)
        )

        query_response = query_response.first() if query_response.first() is not None else None
        ip_address = query_response.ip_address.split("/")[0] if query_response is not None else None
        device_type = query_response.device_type if query_response is not None else None

        url = f"http://{ip_address}:{port}"
        url = url + f"/{endpoint}" if endpoint is not None else url
        local_response = {
            "device_id": device_id,
            "device_type": device_type,
            "ip_address": ip_address,
            "port": port,
            "url": url,
            "request_body": pl,
            "response": {}
        }

        try:
            req_response = requests.post(url=url, json=data)
            local_response["response"]["status_code"] = req_response.status_code
            local_response["response"]["content"] = req_response.json()

        except requests.exceptions.ConnectionError as e:
            local_response["response"]["status_code"] = 500
            local_response["response"]["error"] = "Internal Server Error"
            local_response["response"]["error_message"] = str(e)

        responses.append(local_response)

    return responses
