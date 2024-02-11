from fastapi import FastAPI
import uvicorn

from routers import devices, programs, interactions
from backend.config import ApiSettings

config = ApiSettings()

app = FastAPI(
    title=config.NAME,
    summary=config.SUMMARY,
    description=config.DESCRIPTION,
    version=config.VERSION,
)

app.include_router(devices.router, prefix="/hub")
app.include_router(programs.router, prefix="/hub")
app.include_router(interactions.router)


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=config.PORT)
