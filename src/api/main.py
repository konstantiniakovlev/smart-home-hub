import socket

from fastapi import FastAPI
import uvicorn

from routers import devices
from routers import measurements

HUB_PREFIX = "/hub"

app = FastAPI(
    title="smart-home-hub-api",
    summary="",
    description="",
    version="0.0.1",
)
app.include_router(devices.router, prefix=HUB_PREFIX)
app.include_router(measurements.router, prefix=HUB_PREFIX)


if __name__ == "__main__":
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)

    uvicorn.run(app=app, host=ipaddress, port=5000)
