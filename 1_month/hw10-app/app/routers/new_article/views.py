from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from core.models import Tag
from routers.api.authorization.dependencies import read_authorize_user_or_none
from routers.api.authorization.schemas import User
from routers.api.tag.model import read_all_tags

router = APIRouter(prefix='/new_article',
                   tags=['New article']
                   )

templates = Jinja2Templates(directory="templates")


@router.get('/')
async def new_article(
        request: Request,
        current_user: Annotated[str, Depends(read_authorize_user_or_none)],
        tags: Annotated[Sequence[Tag], Depends(read_all_tags)]
):
    is_light_theme = request.cookies.get('theme', 'dark') == 'light'

    if current_user is None:
        current_user = User(id=-1, username='Login')

    tag_names = [tag.name for tag in tags]

    return templates.TemplateResponse(
        request=request,
        name="new_article.html",
        context={
            'is_light_theme': is_light_theme,
            'current_user': current_user,
            'tags': tag_names,
        }
    )
