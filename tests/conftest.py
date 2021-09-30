import alembic
import asyncio
import pytest
import warnings

from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.db.session import Session

settings = get_settings()


# override the event loop
@pytest.fixture(scope='session')
def event_loop(request):
    """
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# apply migrations at beginning and end of testing session
@pytest.fixture(scope='session')
def apply_migrations():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    config = Config('alembic.ini')

    alembic.command.upgrade(config, 'head')
    yield
    alembic.command.downgrade(config, 'base')


# create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from src.main import get_application

    return get_application()


# make requeests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://testserver',
            headers={'Content-Type': 'application/json'},
        ) as client:
            yield client

