from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/login',
                   tags=['Login']
                   )


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={'login_active': True}
    )