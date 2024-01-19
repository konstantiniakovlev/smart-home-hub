from fastapi import FastAPI
import uvicorn

from routers import devices, programs
from backend.config import ApiSettings

api_config = ApiSettings()

app = FastAPI(
    title=api_config.NAME,
    summary=api_config.SUMMARY,
    description=api_config.DESCRIPTION,
    version=api_config.VERSION,
)

app.include_router(devices.router, prefix="/hub")
app.include_router(programs.router, prefix="/hub")


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=api_config.PORT)
