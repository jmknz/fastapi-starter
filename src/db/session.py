from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=settings.DEBUG)

Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

