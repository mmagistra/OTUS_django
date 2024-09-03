from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from core.models import db_helper
from routers.api.article.model import create_article, delete_post
from routers.api.article.schemas import CreateFormData, DeleteFormData
from routers.api.authorization.dependencies import get_current_active_user_from_db
from routers.api.authorization.schemas import User

router = APIRouter(prefix='/article',
                   tags=['Article']
                   )


@router.post('/create')
async def new_article(
        current_user: Annotated[User, Depends(get_current_active_user_from_db)],
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        form_data: Annotated[CreateFormData, Depends()]
):
    await create_article(
        session=session,
        title=form_data.title,
        subtitle=form_data.subtitle,
        text=form_data.text,
        tags=form_data.tags,
        owner=current_user,
    )
    return status.HTTP_201_CREATED


@router.post('/delete')
async def delete_article(
        current_user: Annotated[User, Depends(get_current_active_user_from_db)],
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        form_data: Annotated[DeleteFormData, Depends()],
):
    if current_user.id == form_data.author_id:
        result = await delete_post(session, form_data.post_id)
        return result
    else:
        return status.HTTP_401_UNAUTHORIZED
