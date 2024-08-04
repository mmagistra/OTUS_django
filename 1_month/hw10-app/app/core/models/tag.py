from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Tag(Base):
    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(255), unique=True)

    # posts: Mapped[List[Post]] = relationship(secondary=association_table)

    def __str__(self):
        return f"(Tag id={self.id}, name={self.name})"