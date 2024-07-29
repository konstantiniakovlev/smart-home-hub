from sqlalchemy import Column, VARCHAR

from models.base import Base


class TagModel(Base):
    __tablename__ = "sensors"

    name = Column(VARCHAR(255), nullable=False)
    tag = Column(VARCHAR(255), nullable=False, primary_key=True)
    description = Column(VARCHAR(255), nullable=True)

    class Config:
        orm_mode = True
