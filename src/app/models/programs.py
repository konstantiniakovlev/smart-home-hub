from sqlalchemy import Column, Integer, VARCHAR

from models.base import Base


class ProgramModel(Base):
    __tablename__ = "program_registry"

    program_id = Column(Integer, primary_key=True, nullable=False)
    device_id = Column(Integer, nullable=False)
    port = Column(Integer, nullable=False)
    description = Column(VARCHAR(255), nullable=True)

    class Config:
        orm_mode = True
