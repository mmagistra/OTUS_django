from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent
DB_PATH = f'{BASE_DIR}/db.sqlite3'


class Settings(BaseSettings):
    db_url: str = f'sqlite+aiosqlite:///{DB_PATH}'
    # echo: bool = False
    echo: bool = True


settings = Settings()
