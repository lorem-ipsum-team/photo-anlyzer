from datetime import datetime, timezone
from sqlalchemy import Column, Boolean, Date, DateTime
from pgvector.sqlalchemy import Vector
from geoalchemy2 import Geography
from app.internal.entity.base import Base


class UserPhoto(Base):
    __tablename__ = 'photos'

    photo = Column(Vector(512), nullable=False)


class UserDescription(Base):
    __tablename__ = 'descriptions'

    tags = Column(Vector(512), nullable=False)


class User(Base):
    __tablename__ = 'users'

    gender = Column(Boolean, nullable=False)
    birthday = Column(Date, nullable=False)


class UserPreference(Base):
    __tablename__ = 'preferences'

    photo = Column(Vector(512), nullable=False)
    tags = Column(Vector(512), nullable=False)


class UserGeo(Base):
    __tablename__ = 'geo'

    location = Column(Geography('POINT', 4326), nullable=False)
    geo_updated = Column(DateTime(timezone=True), nullable=False,
                         default=lambda: datetime.now(timezone.utc))
