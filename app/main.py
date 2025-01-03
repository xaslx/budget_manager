from dishka import make_async_container, AsyncContainer
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.ioc import AppProvider
from app.routers.auth import auth_router
from dishka.integrations import fastapi as fastapi_integration
from app.config import Config



config: Config = Config()
container: AsyncContainer = make_async_container(AppProvider(), context={Config: config})


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield



def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title='Budget Manager',
        description='Это веб-приложение для управления личными финансами',
        lifespan=lifespan,
    )
    app.include_router(router=auth_router, prefix='/api/v1/auth')
    fastapi_integration.setup_dishka(container=container, app=app)
    return app

