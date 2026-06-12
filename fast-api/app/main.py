from fastapi import FastAPI

from .config import settings
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
    )
    app.include_router(router)
    return app


app = create_app()
