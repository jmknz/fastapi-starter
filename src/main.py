from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router as api_router
from src.core.config import get_settings

settings = get_settings()


def get_application():
    app = FastAPI(version=settings.APP_VERSION, title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(api_router, prefix=settings.API_PREFIX)

    @app.get('/', name='heartbeat', tags=['Health Check'])
    async def heartbeat():
        return {'thump': 'thump'}

    return app


app = get_application()

