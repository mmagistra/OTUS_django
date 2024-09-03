from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .model import add_user
from .schemas import Token, TokenData, User, UserInDB, UserForRegister
from .dependencies import *

from core.settings import settings

router = APIRouter(prefix='/authorization',
                   tags=['Authorization']
                   )


@router.post("/token")
async def login_for_access_token(
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post('/registrate', status_code=status.HTTP_201_CREATED)
async def register_new_user(
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    username = form_data.username
    password = form_data.password
    print(username, password)

    hashed_password = hash_password(password)

    try:
        response = await add_user(session, UserInDB(username=username, hashed_password=hashed_password))
    except IntegrityError:
        return status.HTTP_409_CONFLICT

    return response


@router.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
