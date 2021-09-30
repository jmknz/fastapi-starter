import logging

from functools import lru_cache
from pydantic import BaseSettings, validator

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    APP_VERSION: str = '0.1.0'
    APP_NAME: str = 'FastAPI Starter'
    FASTAPI_ENV: str = 'development'
    DEBUG: bool = False
    TESTING: bool = False

    SECRET_KEY: str = 'THIS_IS_A_SECRET!'

    API_PREFIX = '/api'

    DATABASE_URL: str
    @validator('DATABASE_URL', pre=True)
    def get_database_url(cls, v: str):
        return v.split('?')[0]

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings() -> Settings:
    logger.info('Loading config settings from the environment')
    return Settings()

