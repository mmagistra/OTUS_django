import datetime
from typing import Annotated

import humanize
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from core.models import db_helper, User as DbUser
from routers.api.article.model import read_post
from routers.api.authorization.dependencies import read_authorize_user_or_none
from routers.api.authorization.model import get_user_by_id
from routers.api.authorization.schemas import User

router = APIRouter(prefix='/article',
                   tags=['Article']
                   )

templates = Jinja2Templates(directory="templates")


@router.get('/{article_id}/')
async def read_article(
        request: Request,
        article_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        current_user: Annotated[DbUser, Depends(read_authorize_user_or_none)],
):
    is_light_theme = request.cookies.get('theme', 'dark') == 'light'

    if current_user is None:
        current_user = User(id=-1, username='Login')

    article = await read_post(session, article_id)
    if article is None:
        return status.HTTP_404_NOT_FOUND

    delta = datetime.datetime.now() - article.create_data
    delta = humanize.naturaldelta(delta)

    author = await get_user_by_id(session, article.owner_id)

    async with db_helper.engine.begin() as conn:
        tags = await conn.run_sync(
            lambda sync_conn: article.tags
        )
    print(tags)

    return templates.TemplateResponse(
        request=request,
        name='article.html',
        context={
            'is_light_theme': is_light_theme,
            'current_user': current_user,
            'article': {
                'id': article.id,
                'title': article.title,
                'subtitle': article.description,
                'text': article.text,
                'date': str(delta),
                'author': author.username,
                'tags': tags,
            },
            'level': 2,
            'is_author': author.id == current_user.id,
        }
    )
