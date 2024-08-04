import csv
import io
from typing import Annotated

from fastapi import FastAPI
from pydantic import EmailStr

from contextlib import asynccontextmanager

from starlette.staticfiles import StaticFiles

from core.models.db_helper import db_helper
from core.models.base import Base
from create_fastapi_app import create_app

from routers.about.views import router as about_router
from routers.home.views import router as home_router
from routers.profile.views import router as profile_router
from routers.login.views import router as login_router
# from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown


app = create_app(create_custom_static_urls=False, lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(about_router)
app.include_router(home_router)
app.include_router(login_router)
app.include_router(profile_router)
# app.include_router(api_router)


@app.get("/hello/", tags=['Test'])
def hello_world():
    return {"message": "Hello World"}