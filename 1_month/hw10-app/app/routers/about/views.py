from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/about',
                   tags=['About']
                   )


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse(
        request=request, name="about.html", context={'about_active': True}
    )
