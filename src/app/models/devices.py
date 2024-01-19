from sqlalchemy import Column, Integer, String, VARCHAR

from models.base import Base


class DeviceModel(Base):
    __tablename__ = "device_registry"

    device_id = Column(Integer, primary_key=True, nullable=False)
    mac_address = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    device_type = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(255), nullable=True)

    class Config:
        orm_mode = True
