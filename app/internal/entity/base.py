import sqlalchemy as sa
from sqlalchemy import MetaData, UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base(object):
    __name__: str
    metadata: MetaData

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True
    )
