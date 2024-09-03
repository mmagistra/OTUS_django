from sqlalchemy import select, Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User as DbUser
from .schemas import UserInDB


async def add_user(
        session: AsyncSession,
        user: UserInDB,
):
    new_user = DbUser(username=user.username, hashed_password=user.hashed_password)
    session.add(new_user)
    await session.commit()
    await session.close()
    # await session.refresh(product)
    return user


async def get_user_by_username(
        session: AsyncSession,
        username: str
) -> DbUser | None:
    stmt = select(DbUser).where(DbUser.username == username).order_by(DbUser.id)
    result: Result = await session.execute(stmt)
    try:
        user: DbUser = result.scalar_one()
    except NoResultFound:
        return None
    return user


async def get_user_by_id(
        session: AsyncSession,
        user_id: int
) -> DbUser | None:
    stmt = select(DbUser).where(DbUser.id == user_id).order_by(DbUser.id)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()
