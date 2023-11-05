from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.dialects.postgresql import ENUM

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

def to_pg_enum(enum_class) -> ENUM:
    return ENUM(enum_class, name=enum_class.__name__)

@as_declarative()
class Base:
    id = Column(UUID, primary_key=True, index=True, default=func.uuid_generate_v4())
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()