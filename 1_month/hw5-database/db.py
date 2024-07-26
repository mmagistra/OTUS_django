from __future__ import annotations

from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from datetime import datetime

from typing_extensions import List

from db_config import *

engine = create_engine(url=DB_PATH, echo=DB_ECHO)


class Base(DeclarativeBase):
    def __repr__(self):
        return str(self)


association_table = Table(
    "association_table",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column()

    posts: Mapped[List[Post]] = relationship()

    def __str__(self):
        return f"(User id={self.id} username={self.username})"


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(String(1000))
    text: Mapped[str] = mapped_column()
    create_data: Mapped[datetime] = mapped_column()

    tags: Mapped[List[Tag]] = relationship(secondary=association_table)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __str__(self):
        return f"(Post id={self.id} owner_id={self.owner_id})"


class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    # posts: Mapped[List[Post]] = relationship(secondary=association_table)

    def __str__(self):
        return f"(Tag id={self.id}, name={self.name})"


def create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def main():
    create_table()


if __name__ == '__main__':
    main()
