import socket

from fastapi import FastAPI
import uvicorn

from src.api.backend.settings import ApiSettings
from src.api.routers import devices
from src.api.routers import health
from src.api.routers import measurements
from src.api.routers import tags


HUB_PREFIX = "/hub"

app = FastAPI(
    title="smart-home-hub-api",
    summary="",
    description="",
    version=ApiSettings.VERSION
)
app.include_router(devices.router, prefix=HUB_PREFIX)
app.include_router(measurements.router, prefix=HUB_PREFIX)
app.include_router(tags.router, prefix=HUB_PREFIX)
app.include_router(health.router)


if __name__ == "__main__":
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)

    uvicorn.run(app=app, host=ipaddress, port=5000)
