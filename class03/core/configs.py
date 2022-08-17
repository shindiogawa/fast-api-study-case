from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Settings used in the application
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()