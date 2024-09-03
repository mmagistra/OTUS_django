from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Tag


async def read_all_tags(
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)]
) -> Sequence[Tag]:
    stmt = select(Tag).order_by(Tag.id)
    result = await session.execute(stmt)
    tags = result.scalars().all()
    return tags


async def read_tag_by_name(
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        name: str,
) -> Tag:
    stmt = select(Tag).where(Tag.name == name).order_by(Tag.id)
    print(stmt)
    print(name)
    result = await session.execute(stmt)
    tag = result.scalar_one()
    return tag
