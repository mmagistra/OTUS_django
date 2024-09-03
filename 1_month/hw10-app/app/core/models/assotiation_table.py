from sqlalchemy import Table, ForeignKey, Column, Integer

from .base import Base

AssociationTable = Table(
    "association_table",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("post_id", ForeignKey("posts.id")),
    Column("tag_id", ForeignKey("tags.id")),
)
