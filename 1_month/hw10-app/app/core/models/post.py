from datetime import datetime
from typing_extensions import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .assotiation_table import association_table
from .tag import Tag


class Post(Base):
    __tablename__ = 'posts'
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(String(1000))
    text: Mapped[str] = mapped_column()
    create_data: Mapped[datetime] = mapped_column()

    tags: Mapped[List[Tag]] = relationship(secondary=association_table)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __str__(self):
        return f"(Post id={self.id} owner_id={self.owner_id})"
