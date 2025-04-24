from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from app.internal.entity.base import Base


class UserPhoto(Base):
    __tablename__ = 'photos'

    data = Column(JSONB, nullable=False)


class UserDescription(Base):
    __tablename__ = 'descriptions'

    tags = Column(JSONB, nullable=False)
