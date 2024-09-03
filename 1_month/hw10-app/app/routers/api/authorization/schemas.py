from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int = -1
    username: str


class UserForRegister(User):
    password: str


class UserInDB(User):
    hashed_password: str
