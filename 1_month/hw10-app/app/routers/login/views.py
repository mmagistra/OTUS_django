from typing import Annotated

from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from routers.api.authorization.schemas import User
from routers.api.authorization.dependencies import read_authorize_user_or_none

router = APIRouter(prefix='/login',
                   tags=['Login']
                   )

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_login(
        request: Request,
        current_user: Annotated[str, Depends(read_authorize_user_or_none)],
):
    is_light_theme = request.cookies.get('theme', 'dark') == 'light'

    if current_user is None:
        current_user = User(username='Login')
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                'login_active': True,
                'is_light_theme': is_light_theme,
                'current_user': current_user,
            }
        )
    return templates.TemplateResponse(
        request=request,
        name="login_authorized.html",
        context={
            'login_active': True,
            'is_light_theme': is_light_theme,
            'current_user': current_user,
        }
    )
