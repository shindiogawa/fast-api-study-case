from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    DBBaseModel = declarative_base()
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    JWT_SECRET: str = 'I4Hct0Q-_RfcnPp9DY1G5Os71vGxmev4H0Ad6wB7eaA'

    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    
    class Config:
        case_sensitive =  True

settings: Settings = Settings()
