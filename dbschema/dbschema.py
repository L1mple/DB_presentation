from fastdto.common.enums import ColumnTypeEnum
from fastdto.core.dsl.schema.base import Base
from fastdto.core.dsl.schema.column import Column


class Books(Base):
    """User's table."""

    __tablename__ = "books"

    id = Column(column_type=ColumnTypeEnum.INTEGER)  # noqa
    title = Column(column_type=ColumnTypeEnum.TEXT)
    year = Column(column_type=ColumnTypeEnum.INTEGER)
