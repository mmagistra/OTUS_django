import textwrap
from typing import Annotated, Sequence

from fastapi import Request, APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Tag
from routers.api.article.model import read_all_posts, read_posts_by_tags
from routers.api.authorization.dependencies import read_authorize_user_or_none
from routers.api.authorization.schemas import User
from routers.api.tag.model import read_all_tags

router = APIRouter(prefix='/home',
                   tags=['Home']
                   )

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_home(
        request: Request,
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        current_user: Annotated[str, Depends(read_authorize_user_or_none)],
        all_tags: Annotated[Sequence[Tag], Depends(read_all_tags)],
        tags: Annotated[list[str] | None, Query()] = None,
):
    is_light_theme = request.cookies.get('theme', 'dark') == 'light'

    if current_user is None:
        current_user = User(username='Login')

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

    all_posts = await read_posts_by_tags(session=session, tags=tags)
    allow_tags = tags
    if tags is None:
        allow_tags = []

    # cards_list = [example_article]
    cards_list = []

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
        sym_left = 12 * 4
        for tag in tags:
            if len(tag) > 12 and sym_left > 11:
                new_tags.append(tag[:9].lower() + '...')
                sym_left -= 12
            elif len(tag) > sym_left:
                if sym_left > 5:
                    new_tags.append(tag[:sym_left - 3].lower() + '...')
                    sym_left -= len(tag)
            else:
                new_tags.append(tag.lower())
                sym_left -= len(tag)
            if sym_left < 3:
                break
        card['tags'] = new_tags

    tag_names = [tag.name for tag in all_tags]

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            'home_active': True,
            'is_light_theme': is_light_theme,
            'current_user': current_user,
            'cards': cards_list,
            'tags': tag_names,
            'allow_tags': allow_tags,
        }
    )
