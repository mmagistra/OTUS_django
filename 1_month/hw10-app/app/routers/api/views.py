from fastapi import Request, APIRouter, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from .theme.views import router as theme_router
from .authorization.views import router as auth_router
from .article.views import router as article_router


router = APIRouter(prefix='/api',
                   tags=['Api']
                   )
router.include_router(theme_router)
router.include_router(auth_router)
router.include_router(article_router)
