from typing import Sequence, List

from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import Post, Tag, User, AssociationTable

from datetime import datetime

from routers.api.tag.model import read_tag_by_name


async def create_article(
        session: AsyncSession,
        title: str,
        subtitle: str,
        text: str,
        tags: list,
        owner: User
):
    stmt = select(Tag).where(Tag.name.in_(tags))
    result = await session.execute(stmt)
    all_tags = result.scalars().all()
    print(all_tags)
    post = Post(
        title=title,
        description=subtitle,
        text=text,
        create_data=datetime.now(),
        tags=all_tags,
        owner_id=owner.id,
    )
    session.add(post)
    await session.commit()


async def read_all_posts(
        session: AsyncSession,
        user: User | None = None
) -> Sequence[Post]:
    stmt = select(Post)
    if user:
        stmt = stmt.where(Post.owner_id == user.id)
    stmt = stmt.order_by(Post.create_data)
    result = await session.execute(stmt)
    posts = result.scalars().all()
    return posts


async def read_post(
        session: AsyncSession,
        post_id: int
) -> Post | None:
    stmt = select(Post).where(Post.id == post_id).order_by(Post.create_data)
    result = await session.execute(stmt)
    posts = result.scalar_one_or_none()
    return posts


async def read_posts_by_tags(
        session: AsyncSession,
        tags: List[str] | None
) -> Sequence[Post]:
    stmt = select(Post)
    if tags:
        tags = [await read_tag_by_name(session, tag) for tag in tags]
        stmt = stmt.where(and_(*[
            Post.tags.contains(tag) for tag in tags
        ]))
    stmt = stmt.order_by(Post.create_data)
    result = await session.execute(stmt)
    posts = result.scalars().all()
    return posts


async def delete_post(
        session: AsyncSession,
        post_id: int
):
    stmt = delete(Post).where(Post.id == post_id)
    await session.execute(stmt)
    stmt = delete(AssociationTable).where(AssociationTable.c.post_id == post_id)
    await session.execute(stmt)
    await session.commit()
    return status.HTTP_204_NO_CONTENT
