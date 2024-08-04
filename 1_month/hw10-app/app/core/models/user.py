from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import List

from .base import Base
from .post import Post


class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column()

    posts: Mapped[List[Post]] = relationship()

    def __str__(self):
        return f"(User id={self.id} username={self.username})"
