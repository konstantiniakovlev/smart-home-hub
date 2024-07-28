from sqlalchemy import Column, Integer, VARCHAR, DateTime, Float
from sqlalchemy.sql import func

from models.base import Base


class MeasurementModel(Base):
    __tablename__ = "measurements"

    time = Column(DateTime(timezone=True), default=func.now(), primary_key=True)
    device_id = Column(Integer, nullable=False, primary_key=True)
    sensor_tag = Column(VARCHAR(255), nullable=False, primary_key=True)
    value = Column(Float, nullable=False)

    class Config:
        orm_mode = True
