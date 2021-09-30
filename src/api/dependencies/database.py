from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Type

from src.db.repositories.base import BaseRepository
from src.db.session import Session


async def get_session() -> AsyncSession:
    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_repository(RepoType: Type[BaseRepository]) -> Callable:
    def get_repo(session: AsyncSession = Depends(get_session)) -> Type[BaseRepository]:
        return RepoType(session)

    return get_repo

