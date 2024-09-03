import textwrap
from typing import Annotated, Sequence

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Post, db_helper, User as DbUser
from routers.api.authorization.dependencies import read_authorize_user_or_none
from routers.api.authorization.schemas import User
from routers.api.article.model import read_all_posts

router = APIRouter(prefix='/profile',
                   tags=['Profile']
                   )


templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_profile(
        request: Request,
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        current_user: Annotated[DbUser, Depends(read_authorize_user_or_none)],
        is_new_article_added: bool = False,
        is_article_deleted: bool = False
):
    is_light_theme = request.cookies.get('theme', 'dark') == 'light'

    if current_user is None:
        current_user = User(username='Login')
        return templates.TemplateResponse(
            request=request,
            name="unauthorized_profile.html",
            context={
                'profile_active': True,
                'is_light_theme': is_light_theme,
                'current_user': current_user,
            }
        )

    # tag = f'{"k"*9}...'.lower()

    example_article = {
            'title': 'Card title',
            'subtitle': 'Card subtitle',
            'text': "Some quick example text to build on the card title and make up the bulk of the card's content.",
            'tags': [
                'Tag 1',
                'Tag 2',
                'Tag 3',
                'Tag 4',
            ],
            'id': 1,
        }

    all_posts = await read_all_posts(session=session, user=current_user)

    cards_list = [example_article]

    for post in all_posts:
        async with db_helper.engine.begin() as conn:
            tags = await conn.run_sync(
                lambda sync_conn: post.tags
            )

        card = {
            'id': post.id,
            'title': textwrap.shorten(post.title, width=35, placeholder="..."),
            'subtitle': textwrap.shorten(post.description, width=40, placeholder="..."),
            'text': textwrap.shorten(post.text, width=400, placeholder="..."),
            'tags': [tag.name for tag in tags],
            'create_data': post.create_data,
        }
        cards_list.append(card)

    for card in cards_list:
        tags = card.get('tags', [])
        new_tags = []
        sym_left = 12*4
        for tag in tags:
            if len(tag) > 12 and sym_left > 11:
                new_tags.append(tag[:9].lower()+'...')
                sym_left -= 12
            elif len(tag) > sym_left:
                if sym_left > 5:
                    new_tags.append(tag[:sym_left-3].lower()+'...')
                    sym_left -= len(tag)
            else:
                new_tags.append(tag.lower())
                sym_left -= len(tag)
            if sym_left < 3:
                break
        card['tags'] = new_tags

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            'profile_active': True,
            'is_light_theme': is_light_theme,
            'current_user': current_user,
            'cards': cards_list,
            'is_new_article_added': is_new_article_added,
            'is_article_deleted': is_article_deleted,
        }
    )