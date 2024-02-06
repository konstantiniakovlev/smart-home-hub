from sqlalchemy import Column, Integer, Identity, VARCHAR, DateTime
from sqlalchemy.sql import func

from models.base import Base


class ProgramModel(Base):
    __tablename__ = "program_registry"

    program_id = Column(Integer, Identity(always=True), primary_key=True)
    device_id = Column(Integer, nullable=False)
    port = Column(Integer, nullable=True)
    program_name = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(255), nullable=True)
    registered_at = Column(DateTime(timezone=False), default=func.now())
    updated_at = Column(DateTime(timezone=False), default=func.now(), onupdate=func.now())

    class Config:
        orm_mode = True
