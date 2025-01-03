from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn



@asynccontextmanager
async def lifespan(app: FastAPI):

    yield



def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title='Budget Manager',
        description='Это веб-приложение для управления личными финансами',
        lifespan=lifespan,
    )
    return app


if __name__ == '__main__':
    uvicorn.run(create_app)