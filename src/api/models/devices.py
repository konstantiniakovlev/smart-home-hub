from sqlalchemy import Column, Integer, String, VARCHAR, Identity, DateTime
from sqlalchemy.sql import func

from models.base import Base


class DeviceModel(Base):
    __tablename__ = "device_registry"

    device_id = Column(Integer, Identity(always=True), primary_key=True)
    mac_address = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    device_type = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(255), nullable=True)
    registered_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    class Config:
        orm_mode = True
