from os import getenv
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"

DB_URL = getenv('DATABASE_URL', f"sqlite+aiosqlite:///{DB_PATH}")
CURRENT_SETTINGS = getenv('SETTINGS', 'Settings')

print('OUR DB URL IS ', DB_URL)


class Settings(BaseSettings):
    db_url: str = DB_URL
    echo: bool = False
    # echo: bool = True

    # JWT
    SECRET_KEY: str = "20df8537a9ffe6efdc5df0cf63a7f797ba294779c79f4c59edd5a17dee98d774"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class TestSettings(BaseSettings):
    db_url: str = DB_URL
    # echo: bool = False
    echo: bool = False


class ProdSettings(TestSettings):
    pass


settings_dict = {
    'Settings': Settings,
    'TestSettings': TestSettings
}


settings = settings_dict.get(CURRENT_SETTINGS, Settings)()
