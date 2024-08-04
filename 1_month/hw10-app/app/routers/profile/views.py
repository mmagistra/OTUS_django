from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/profile',
                   tags=['Profile']
                   )


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_profile(request: Request):
    return templates.TemplateResponse(
        request=request, name="profile.html", context={'profile_active': True}
    )